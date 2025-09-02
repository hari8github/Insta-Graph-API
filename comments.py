import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get access token from environment variables
access_token = os.getenv('ACCESS_TOKEN')

# Step 1: Fetch user media
media_url = 'https://graph.instagram.com/me/media'
media_params = {
    'fields': 'id,media_type,media_url,caption,timestamp',
    'access_token': access_token
}

media_response = requests.get(media_url, params=media_params)

# Check if the media request was successful
if media_response.status_code == 200:
    media_data = media_response.json().get('data', [])
    print("Media Items:")
    for media in media_data:
        print(f"Media ID: {media['id']}")
        print(f"Media Type: {media['media_type']}")
        print(f"Media URL: {media.get('media_url', 'N/A')}")
        print(f"Caption: {media.get('caption', 'N/A')}")
        print(f"Timestamp: {media['timestamp']}")

        # Step 2: Fetch comments for this media item
        comments_url = f"https://graph.instagram.com/{media['id']}/comments"
        comments_params = {
            'fields': 'text,username,timestamp',
            'access_token': access_token
        }
        comments_response = requests.get(comments_url, params=comments_params)

        # Check if the comments request was successful
        if comments_response.status_code == 200:
            comments_data = comments_response.json().get('data', [])
            if comments_data:
                print("Comments:")
                for comment in comments_data:
                    print(f"  - {comment['username']}: {comment['text']} ({comment['timestamp']})")
            else:
                print("No comments found.")
        else:
            print(f"Error fetching comments: {comments_response.status_code}")
            print(comments_response.text)
        print("-" * 50)
else:
    print(f"Error fetching media: {media_response.status_code}")
    print(media_response.text)