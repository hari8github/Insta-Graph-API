import requests
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

# Create media container
url = f'https://graph.instagram.com/me/media'
params = {
    'image_url': 'https://assets1.cbsnewsstatic.com/hub/i/r/2025/07/03/ddaca1bb-66f4-4c74-abcf-2d468795b3bc/thumbnail/640x464/35857c37593a77447b9125a4febe0474/diogo-jota-liverpool-jpg.jpg',
    'caption': 'Image of a evergreen player. #dj20',
    'access_token': access_token
}

response = requests.post(url, params=params)

if response.status_code == 200:
    container_id = response.json().get('id')
    print(f"Container ID: {container_id}")
else:
    print(f"Error creating container: {response.status_code}")
    print(response.text)

    # Publish the container
publish_url = f'https://graph.instagram.com/me/media_publish'
publish_params = {
    'creation_id': container_id,
    'access_token': access_token
}

publish_response = requests.post(publish_url, params=publish_params)

if publish_response.status_code == 200:
    media_id = publish_response.json().get('id')
    print(f"Successfully published! Media ID: {media_id}")
else:
    print(f"Error publishing: {publish_response.status_code}")
    print(publish_response.text)