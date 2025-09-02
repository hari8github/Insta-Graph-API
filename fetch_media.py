import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get access token from environment variables
access_token = os.getenv('ACCESS_TOKEN')

# Instagram Graph API endpoint for user media
url = 'https://graph.instagram.com/me/media'
params = {
    'fields': 'id,media_type,media_url,caption,timestamp',
    'access_token': access_token
}

# Make GET request to fetch media
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    media_data = response.json().get('data', [])
    print("Media Items:")
    for media in media_data:
        print(f"Media ID: {media['id']}")
        print(f"Media Type: {media['media_type']}")
        print(f"Media URL: {media.get('media_url', 'N/A')}")
        print(f"Caption: {media.get('caption', 'N/A')}")
        print(f"Timestamp: {media['timestamp']}")
        print("-" * 50)
else:
    print(f"Error: {response.status_code}")
    print(response.text)