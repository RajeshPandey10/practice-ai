from models.content_model import ContentModel

class ContentController:
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers, lr):
        self.model = ContentModel(vocab_size, embedding_dim, hidden_dim, num_layers, lr)

    def train_model(self, X, Y, epochs):
        self.model.train(X, Y, epochs)

    def generate_caption(self, seed, char2idx, idx2char, length=100, temperature=1.0):
        return self.model.generate_text(seed, char2idx, idx2char, length, temperature)

    def fetch_trends(self):
        """Fetch real-time trends using the model."""
        return self.model.fetch_trends()

    def generate_captions(self, prompt):
        """Generate captions and hashtags based on a prompt."""
        return self.model.generate_captions(prompt)

    def process_media(self, media_path):
        """Process user-uploaded media using the model."""
        return self.model.process_media(media_path)

    def generate_captions_and_hashtags(self, media_path):
        """Generate captions, hashtags, and trending music based on uploaded media."""
        # Process the media (e.g., extract features, analyze content)
        processed_media = self.model.process_media(media_path)

        # Generate captions and hashtags
        caption = self.model.generate_captions(f"Analyze this media: {processed_media}")
        hashtags = "#viral #trending #AI"  # Placeholder for generated hashtags

        # Suggest trending music (mocked for now)
        trending_music = "Top Trending Song - Artist Name"

        return {
            "caption": caption,
            "hashtags": hashtags,
            "music": trending_music
        }
