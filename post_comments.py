import requests
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

def post_comment(media_id, comment_text):
    url = f'https://graph.instagram.com/{media_id}/comments'
    params = {
        'message': comment_text,
        'access_token': access_token
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        comment_id = response.json().get('id')
        print(f"Comment posted successfully! Comment ID: {comment_id}")
        return comment_id
    else:
        print(f"Error posting comment: {response.status_code}")
        print(response.text)
        return None

# Usage
media_id = "17923978806122881"  # Get this from your media fetch or after posting
comment_text = "Miss you jota "
post_comment(media_id, comment_text)