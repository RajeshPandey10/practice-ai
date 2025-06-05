# Flask-based application
from flask import Flask, request, render_template
from controllers.content_controller import ContentController
import os

app = Flask(__name__)
controller = ContentController(vocab_size=100, embedding_dim=128, hidden_dim=256, num_layers=2, lr=0.001)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trends', methods=['GET'])
def display_trends():
    trends = controller.fetch_trends()
    return render_template('trends.html', trends=trends)

@app.route('/upload', methods=['GET', 'POST'])
def upload_media():
    if request.method == 'POST':
        if 'media' not in request.files:
            return "No file uploaded", 400
        media = request.files['media']
        result = controller.process_media(media.filename)
        return render_template('upload.html', result=result)
    return render_template('upload.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate_captions():
    if request.method == 'POST':
        # Ensure the uploads directory exists
        os.makedirs('uploads', exist_ok=True)

        # Handle media upload
        media = request.files.get('media')
        if media:
            media_path = f"uploads/{media.filename}"
            media.save(media_path)
            # Process media and generate content
            result = controller.generate_captions_and_hashtags(media_path)
            return render_template('generate.html', result=result)

        # Handle text-based prompt
        prompt = request.form.get('prompt')
        if prompt:
            result = controller.generate_captions(prompt)
            return render_template('generate.html', result=result)

    return render_template('generate.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')