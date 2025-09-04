import requests
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

def get_user_info():
    """Fetch user basic information"""
    url = 'https://graph.instagram.com/me'
    params = {
        'fields': 'user_id,username',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching user info: {response.status_code}")
        return None

def get_media_insights(media_id, media_type, media_product_type):
    """Fetch insights based on media type and product type"""
    url = f'https://graph.instagram.com/{media_id}/insights'
    
    # Metrics based on type (avoid deprecated ones like plays, video_views, clips_replays_count)
    if media_type == 'VIDEO' and media_product_type == 'REELS':
        metrics = 'reach,likes,comments,saved,shares,ig_reels_video_view_total_time,ig_reels_avg_watch_time,views'
    elif media_type == 'VIDEO':
        metrics = 'reach,likes,comments,saved,shares,views'
    else:
        # For photos and carousels (note: carousels may return no data)
        metrics = 'reach,likes,comments,saved,shares'
    
    params = {
        'metric': metrics,
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        insights_data = response.json().get('data', [])
        insights = {}
        for insight in insights_data:
            insights[insight['name']] = insight['values'][0]['value']
        return insights
    else:
        print(f"Insights error for {media_id}: {response.status_code}")
        return {}

def get_media_comments(media_id):
    """Fetch comments for a specific media"""
    url = f"https://graph.instagram.com/{media_id}/comments"
    params = {
        'fields': 'text,username,timestamp',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return []

def format_duration(seconds):
    """Convert seconds to readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def analyze_instagram_account():
    """Complete Instagram account analysis"""
    print("=" * 80)
    print("INSTAGRAM COMPLETE ANALYTICS DASHBOARD")
    print("=" * 80)
    
    # Get user info
    user_info = get_user_info()
    if not user_info:
        return
    
    print(f"\n📊 ACCOUNT DETAILS")
    print(f"Username: @{user_info['username']}")
    print(f"User ID: {user_info['user_id']}")
    print("-" * 80)
    
    # Get user media (includes media_product_type)
    media_url = 'https://graph.instagram.com/me/media'
    media_params = {
        'fields': 'id,media_type,media_product_type,media_url,caption,timestamp,like_count,comments_count,permalink',
        'access_token': access_token
    }
    
    media_response = requests.get(media_url, params=media_params)
    
    if media_response.status_code != 200:
        print(f"Error fetching media: {media_response.status_code}")
        return
    
    media_data = media_response.json().get('data', [])
    
    print(f"\n📈 POSTS ANALYSIS ({len(media_data)} posts)")
    print("-" * 80)
    
    # Statistics tracking
    total_likes = 0
    total_comments = 0
    total_reach = 0
    total_saved = 0
    total_shares = 0
    total_views = 0  # Unified for videos/Reels
    
    post_types = {'IMAGE': 0, 'VIDEO': 0, 'CAROUSEL_ALBUM': 0, 'REELS': 0}
    
    for i, media in enumerate(media_data, 1):
        media_type = media['media_type']
        media_product_type = media.get('media_product_type', 'FEED')  # Default to FEED if missing
        
        # Track Reels separately for display
        display_type = 'REELS' if media_product_type == 'REELS' else media_type
        post_types[display_type] = post_types.get(display_type, 0) + 1
        
        print(f"\n📱 POST #{i} - {display_type}")
        print(f"ID: {media['id']}")
        print(f"Posted: {media['timestamp']}")
        print(f"Permalink: {media.get('permalink', 'N/A')}")
        
        # Caption
        caption = media.get('caption', 'No caption')
        if len(caption) > 150:
            caption = caption[:150] + "..."
        print(f"Caption: {caption}")
        
        # Basic metrics
        likes = media.get('like_count', 0)
        comments_count = media.get('comments_count', 0)
        print(f"❤️  Likes: {likes}")
        print(f"💬 Comments: {comments_count}")
        
        total_likes += likes
        total_comments += comments_count
        
        # Get insights
        insights = get_media_insights(media['id'], media_type, media_product_type)
        
        if insights:
            reach = insights.get('reach', 0)
            saved = insights.get('saved', 0)
            shares = insights.get('shares', 0)
            
            print(f"👥 Reach: {reach}")
            print(f"💾 Saved: {saved}")
            print(f"🔄 Shares: {shares}")
            
            total_reach += reach
            total_saved += saved
            total_shares += shares
            
            # Video/Reel-specific metrics
            if media_type == 'VIDEO':
                views = insights.get('views', 0)
                print(f"👁️  Views: {views}")
                total_views += views
                
                if media_product_type == 'REELS':
                    total_watch_time = insights.get('ig_reels_video_view_total_time', 0)
                    avg_watch_time = insights.get('ig_reels_avg_watch_time', 0)
                    
                    if total_watch_time > 0:
                        print(f"⏱️  Total Watch Time: {format_duration(total_watch_time)}")
                    if avg_watch_time > 0:
                        print(f"⏱️  Avg Watch Time: {format_duration(avg_watch_time)}")
                    
                    # Estimated completion
                    if views > 0 and avg_watch_time > 0 and total_watch_time > 0:
                        estimated_duration = total_watch_time / views if views > 0 else 0
                        if estimated_duration > 0:
                            completion_rate = (avg_watch_time / estimated_duration) * 100
                            print(f"✅ Completion Rate: {completion_rate:.2f}%")
                            print(f"📊 Watch Percentage: {completion_rate:.2f}%")
            
            # Standard engagement rate
            if reach > 0:
                engagement_rate = ((likes + comments_count + saved + shares) / reach) * 100
                print(f"📈 Engagement Rate: {engagement_rate:.2f}%")
        
        # Get comments
        if comments_count > 0:
            comments = get_media_comments(media['id'])
            print(f"\n💬 COMMENTS ({len(comments)}):")
            for comment in comments[:3]:  # Show first 3 comments
                comment_text = comment.get('text', 'N/A')
                if len(comment_text) > 60:
                    comment_text = comment_text[:60] + "..."
                print(f"  @{comment.get('username', 'Unknown')}: {comment_text}")
            if len(comments) > 3:
                print(f"  ... and {len(comments) - 3} more comments")
        
        print("-" * 50)
    
    # Overall summary
    print(f"\n📊 COMPREHENSIVE STATISTICS")
    print("=" * 80)
    
    print(f"📱 Content Breakdown:")
    for post_type, count in post_types.items():
        if count > 0:
            print(f"  {post_type}: {count} posts")
    
    print(f"\n📈 Engagement Totals:")
    print(f"  Total Likes: {total_likes}")
    print(f"  Total Comments: {total_comments}")
    print(f"  Total Reach: {total_reach}")
    print(f"  Total Saved: {total_saved}")
    print(f"  Total Shares: {total_shares}")
    
    if total_views > 0:
        print(f"\n🎬 Video/Reel Performance:")
        print(f"  Total Views: {total_views}")
    
    if media_data:
        print(f"\n📊 Averages per Post:")
        print(f"  Likes: {total_likes / len(media_data):.1f}")
        print(f"  Comments: {total_comments / len(media_data):.1f}")
        if total_reach > 0:
            print(f"  Reach: {total_reach / len(media_data):.1f}")
            print(f"  Saved: {total_saved / len(media_data):.1f}")
            print(f"  Shares: {total_shares / len(media_data):.1f}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_instagram_account()