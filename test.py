import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get access token from environment variables
access_token = os.getenv('ACCESS_TOKEN')

# Instagram Graph API endpoint
url = 'https://graph.instagram.com/me'
params = {
    'fields': 'user_id,username',
    'access_token': access_token
}

# Make GET request
response = requests.get(url, params=params)

# Print response with headers
print(f"Status Code: {response.status_code}")
print("Headers:")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print("\nBody:")
print(response.text)