import requests
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

def get_post_insights(media_id):
    url = f'https://graph.instagram.com/{media_id}/insights'
    params = {
        'metric': 'reach,likes,comments,saved,shares,profile_visits,follows,total_interactions',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        insights_data = response.json().get('data', [])
        for insight in insights_data:
            metric_name = insight['name']
            metric_value = insight['values'][0]['value']
            print(f"{metric_name}: {metric_value}")
        return insights_data
    else:
        print(f"Error fetching insights: {response.status_code}")
        print(response.text)
        return None

# Usage
media_id = "17961529394973346"
get_post_insights(media_id)