from controllers.content_controller import ContentController

class AppView:
    def __init__(self, controller):
        self.controller = controller

    def upload_media(self):
        # Placeholder for media upload logic
        print("Media uploaded successfully!")

    def display_generated_caption(self, caption):
        print("\nGenerated Caption:")
        print(caption)

    def display_trends(self):
        """Display real-time trends fetched from the controller."""
        trends = self.controller.fetch_trends()
        print("\nReal-Time Trends:")
        for trend in trends:
            print(f"- {trend}")

    def upload_and_process_media(self):
        """Upload media and display processed results."""
        media_path = input("Enter the path to your media file: ")
        result = self.controller.process_media(media_path)
        print(f"\nMedia Processing Result: {result}")

    def generate_captions_and_hashtags(self):
        """Generate captions and hashtags based on user input."""
        prompt = input("Enter a prompt for caption generation: ")
        caption = self.controller.generate_captions(prompt)
        print(f"\nGenerated Caption and Hashtags: {caption}")

    def run(self, char2idx, idx2char):
        while True:
            print("\nMenu:")
            print("1. Display Real-Time Trends")
            print("2. Upload and Process Media")
            print("3. Generate Captions and Hashtags")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.display_trends()
            elif choice == "2":
                self.upload_and_process_media()
            elif choice == "3":
                self.generate_captions_and_hashtags()
            elif choice == "4":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")
