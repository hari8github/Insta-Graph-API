# 📌 Instagram Graph API Guide

## 🔐 Core Setup Pattern

All scripts follow this authentication pattern:

```python
import requests, os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
```

### How it works:

- `load_dotenv()` loads environment variables from a `.env` file.
- `ACCESS_TOKEN` should be stored in `.env`:
  ```
  ACCESS_TOKEN=your_token_here
  ```
- This keeps your sensitive token out of your code.

---

## 🌐 API Request Structure

Standard request format for all endpoints:

```python
response = requests.get(url, params={
    'fields': 'field1,field2,field3',
    'access_token': access_token
})

if response.status_code == 200:
    data = response.json().get('data', [])
    # Process data
else:
    print(f"Error: {response.status_code}")
```

---

## 🔑 Key Endpoints & Use Cases

### 1. **User Profile** (`/me`)

- **Purpose**: Test connection and get basic user info
- **Example**:
```python
url = 'https://graph.instagram.com/me'
fields = 'user_id,username'
```

---

### 2. **User Media** (`/me/media`)

- **Purpose**: Fetch all posts from user's account
- **Example**:
```python
url = 'https://graph.instagram.com/me/media'
fields = 'id,media_type,media_product_type,media_url,caption,timestamp,like_count,comments_count,permalink,tags,children'
```

**Additional Fields**:
- `media_product_type`: Distinguishes Reels (`REELS`) from feed posts (`FEED`)
- `tags`: Tagged usernames
- `children`: For carousels
- `permalink`: Direct post link

---

### 3. **Post Comments** (`/{media_id}/comments`)

- **Purpose**: Get comments for a specific post
- **Example**:
```python
url = f'https://graph.instagram.com/{media_id}/comments'
fields = 'text,username,timestamp,replies'
```

**Additional Fields**:
- `replies`: Threaded comment replies

---

### 4. **Media Insights** (`/{media_id}/insights`)

- **Purpose**: Fetch engagement/performance metrics (Business/Creator accounts only)
- **Example**:
```python
url = f'https://graph.instagram.com/{media_id}/insights'
fields = 'reach,likes,comments,saved,shares,total_interactions,profile_visits,follows,profile_activity'  # For photos/carousels
fields = 'reach,likes,comments,saved,shares,views,ig_reels_video_view_total_time,ig_reels_avg_watch_time,total_interactions,profile_visits,follows,profile_activity'  # For Reels
```

**How it works**:
- Requires `instagram_business_manage_insights` permission
- Metrics vary by media type and product type
- Reels-specific: `views`, `ig_reels_video_view_total_time`, `ig_reels_avg_watch_time`

---

### 5. **Create Media Container** (`/me/media` - POST)

- **Purpose**: Prepare an image/video for posting
- **Example**:
```python
url = 'https://graph.instagram.com/me/media'
params = {
    'image_url': 'https://example.com/image.jpg',
    'caption': 'Your caption text #hashtags',
    'access_token': access_token
}
response = requests.post(url, params=params)
```

---

### 6. **Publish Media** (`/me/media_publish` - POST)

- **Purpose**: Publish the prepared media
- **Example**:
```python
url = 'https://graph.instagram.com/me/media_publish'
params = {
    'creation_id': container_id,
    'access_token': access_token
}
response = requests.post(url, params=params)
```

---

### 7. **Add Comment** (`/{media_id}/comments` - POST)

- **Purpose**: Add a comment to a specific post
- **Example**:
```python
url = f'https://graph.instagram.com/{media_id}/comments'
params = {
    'message': comment_text,
    'access_token': access_token
}
response = requests.post(url, params=params)
```

---

### 8. **Complete Account Analysis** (`everything.py`)

- **Purpose**: Comprehensive Instagram analytics for campaign insights
- **Features**:
  - Fetch user info, all media, comments, insights
  - Analyze engagement: likes, comments, reach, saved, shares, views
  - Detect Reels vs Feed
  - Generate dashboard
  - Compute engagement rate
  - Format watch time metrics
  - Suggest content strategies

```python
from everything import analyze_instagram_account
analyze_instagram_account()
```

---

## 🧠 Data Processing Pattern

### 🔁 Nested API Calls

```python
for media in media_data:
    media_id = media['id']
    comments_response = requests.get(comments_url, params=comments_params)
    insights_response = requests.get(insights_url, params=insights_params)
    comments_data = comments_response.json().get('data', [])
    insights_data = insights_response.json().get('data', [])
```

### 🪜 Two-Step Publishing

**Step 1: Container Creation**

- Validate content
- Return `container_id`

**Step 2: Media Publishing**

- Uses `container_id` to post
- Returns `media_id`

---

## 📋 Common Field Options

| Endpoint            | Fields                                                                                 |
|---------------------|-----------------------------------------------------------------------------------------|
| `/me`               | `user_id`, `username`                                                                  |
| `/me/media`         | `id`, `media_type`, `media_product_type`, `media_url`, `caption`, `timestamp`, `like_count`, `comments_count`, `permalink`, `tags`, `children` |
| `/{id}/comments`    | `text`, `username`, `timestamp`, `replies`                                             |
| `/{id}/insights`    | `reach`, `likes`, `comments`, `saved`, `shares`, `views`, `ig_reels_video_view_total_time`, `ig_reels_avg_watch_time`, `total_interactions`, `profile_visits`, `follows`, `profile_activity` |

---

## ⚠️ Error Handling Best Practice

```python
if response.status_code == 200:
    data = response.json()
    print(f"Success: {data}")
else:
    print(f"Error {response.status_code}: {response.text}")
```

---

## 🛑 Important Requirements & Limitations

### Image Requirements
- Must be publicly accessible HTTPS URL
- Formats: JPG, PNG
- Max size: 8MB
- No auth required for access

### Caption Requirements
- Max 2,200 characters
- Hashtags count
- Line breaks allowed using `\n`

### Access Token
- Tokens expire
- Requires proper permissions
- Test with `/me` endpoint

### Rate Limiting
- Instagram enforces hourly limits
- Add delays for bulk tasks
- Monitor status codes