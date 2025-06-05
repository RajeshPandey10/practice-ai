import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import requests
from transformers import pipeline

class CharLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embed(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out[:, -1, :])
        return out, hidden

class ContentModel:
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers, lr):
        self.model = CharLSTM(vocab_size, embedding_dim, hidden_dim, num_layers)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def train(self, X, Y, epochs):
        for epoch in range(epochs):
            output, _ = self.model(X)
            loss = self.criterion(output, Y)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    def generate_text(self, seed, char2idx, idx2char, length=100, temperature=1.0):
        self.model.eval()
        result = seed
        input_seq = torch.tensor([[char2idx[c] for c in seed]])
        hidden = None
        for _ in range(length):
            with torch.no_grad():
                output, hidden = self.model(input_seq, hidden)
                logits = output[0] / temperature
                prob = torch.nn.functional.softmax(logits, dim=0).numpy()
                next_idx = np.random.choice(len(prob), p=prob)
                result += idx2char[next_idx]
                input_seq = torch.cat([input_seq[:, 1:], torch.tensor([[next_idx]])], dim=1)
        return result

    def fetch_trends(self):
        """Fetch real-time trends from Reddit API."""
        url = "https://oauth.reddit.com/api/v1/trending_subreddits"
        headers = {
            "Authorization": "Bearer <access_token>",  # Replace <access_token> with a valid token
            "User-Agent": "TrendFetcher/1.0"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return [subreddit['name'] for subreddit in data.get('subreddit_names', [])]
            else:
                print(f"Failed to fetch trends. Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return []

    def generate_captions(self, prompt):
        """Generate captions and hashtags using an LLM."""
        generator = pipeline("text-generation", model="gpt2")  # Using a public model for testing
        result = generator(prompt, max_length=50, num_return_sequences=1)
        return result[0]['generated_text']

    def process_media(self, media_path):
        """Process user-uploaded images or videos."""
        # Placeholder for media processing logic
        # For example, extract metadata or use OCR for images
        return f"Processed media at {media_path}"
