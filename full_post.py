import requests, os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')

url = "https://graph.instagram.com/me/media"
params = {
    'fields' : 'id, media_type, media_url, caption, timestamp, like_count, comments_count',
    'access_token' : access_token
}

response = requests.get(url, params = params)

if response.status_code == 200:
    data = response.json().get('data', [])
    print("Media Items: ")
    for media in data:
        print(f"POST ID: {media['id']}")
        print(f"Media Type: {media['media_type']}")
        print(f"Media URL: {media.get('media_url', 'N/A')}")
        print(f"Caption: {media.get('caption', 'N/A')}")
        print(f"Timestamp: {media['timestamp']}")
        print(f"Likes: {media.get('like_count', 0)}")
        print(f"Comments Count: {media.get('comments_count', 0)}")

        comments_url = f"https://graph.instagram.com/{media.get('id', 'N/A')}/comments"
        comments_params = {
            'fields': 'text,username,timestamp',
            'access_token': access_token
        }

        comments_response = requests.get(comments_url, params=comments_params)

        if comments_response.status_code == 200:
            comments_data = comments_response.json().get('data', [])
            if comments_data:
                print("Comments:")
                for comment in comments_data:
                    print(f"  - {comment.get('username', 'Unknown')}: {comment.get('text', 'N/A')} ({comment.get('timestamp', 'N/A')})")
            else:
                print("No comments found. Very sad!")
        else:
            print(f"Error fetching comments: {comments_response.status_code}")
            print(comments_response.text)
        print("-" * 50)
else:
    print(f"Error fetching media: {response.status_code}")
    print(response.text)