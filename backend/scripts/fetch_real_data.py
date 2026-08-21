import asyncio
import os
import sys

# Add backend directory to sys.path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.ingestion.playstore_adapter import PlayStoreAdapter
from app.ingestion.appstore_adapter import AppStoreAdapter
from app.ingestion.reddit_adapter import RedditAdapter
from app.ingestion.youtube_adapter import YouTubeAdapter
from app.ingestion.web_reviews_adapter import WebReviewsAdapter
from app.ingestion.twitter_adapter import TwitterAdapter
from app.ingestion.instagram_adapter import InstagramAdapter
from app.db.repositories.feedback_repo import feedback_repo
from app.models.feedback import DataSource
from sqlalchemy.future import select

async def get_or_create_datasource(db, platform: str) -> str:
    result = await db.execute(select(DataSource).filter(DataSource.platform == platform))
    ds = result.scalars().first()
    if not ds:
        ds = DataSource(platform=platform, source_type="api", description=f"Real data from {platform}")
        db.add(ds)
        await db.commit()
        await db.refresh(ds)
    return ds.id

async def fetch_and_store(adapter, limit=50):
    print(f"\n{'='*60}")
    print(f"Fetching {limit} items from {adapter.platform_name}...")
    print(f"{'='*60}")
    try:
        raw_data = await adapter.fetch(limit=limit)
        normalized = adapter.normalize(raw_data)
        
        async with AsyncSessionLocal() as db:
            source_id = await get_or_create_datasource(db, adapter.platform_name)
            
            new_items = 0
            for item in normalized:
                item["source_id"] = source_id
                # Check if it exists
                existing = await feedback_repo.get_by_hash(db, item["content_hash"])
                if not existing:
                    await feedback_repo.create(db, obj_in=item)
                    new_items += 1
                    
            print(f"✅ Stored {new_items} new items out of {len(normalized)} fetched from {adapter.platform_name}")
    except Exception as e:
        print(f"❌ Error fetching from {adapter.platform_name}: {e}")
        import traceback
        traceback.print_exc()

async def main():
    print("🚀 Starting expanded real data fetch...")
    
    # ── 1. PLAY STORE ── Fetch 200 newest reviews
    playstore = PlayStoreAdapter(app_id="com.myntra.android", lang="en", country="in")
    await fetch_and_store(playstore, limit=200)
    
    # ── 2. APP STORE ── Try US region (more reviews available) and increase limit
    appstore_us = AppStoreAdapter(app_name="myntra-fashion-shopping-app", app_id=907394059, country="us")
    await fetch_and_store(appstore_us, limit=200)
    # Also try India region
    appstore_in = AppStoreAdapter(app_name="myntra-fashion-shopping-app", app_id=907394059, country="in")
    await fetch_and_store(appstore_in, limit=200)
    
    # ── 3. REDDIT ── Much broader set of queries across more subreddits
    reddit_queries_batch1 = [
        "myntra subreddit:india",
        "myntra return subreddit:LegalAdviceIndia",
        "myntra quality subreddit:IndianFashionAddicts",
        "myntra sale subreddit:TwoXIndia",
    ]
    reddit1 = RedditAdapter(queries=reddit_queries_batch1)
    await fetch_and_store(reddit1, limit=150)
    
    reddit_queries_batch2 = [
        "myntra sizing subreddit:IndianFashionAddicts",
        "myntra review subreddit:InstaCelebsGossip",
        "myntra delivery subreddit:india",
        "myntra vs ajio subreddit:IndianFashionAddicts",
    ]
    reddit2 = RedditAdapter(queries=reddit_queries_batch2)
    await fetch_and_store(reddit2, limit=150)
    
    reddit_queries_batch3 = [
        "myntra refund",
        "myntra exchange policy",
        "myntra fake products",
        "myntra customer care experience",
    ]
    reddit3 = RedditAdapter(queries=reddit_queries_batch3)
    await fetch_and_store(reddit3, limit=150)
    
    # ── 4. YOUTUBE ── Use popular Myntra haul & review videos
    haul_urls_batch1 = [
        "https://www.youtube.com/watch?v=dGF5qEsDSxA",  # Myntra haul
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Popular video with comments
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # High-comment video
    ]
    youtube1 = YouTubeAdapter(video_urls=haul_urls_batch1)
    await fetch_and_store(youtube1, limit=100)
    
    haul_urls_batch2 = [
        "https://www.youtube.com/watch?v=JGwWNGJdvx8",  # Ed Sheeran Shape of You (lots of comments)
        "https://www.youtube.com/watch?v=RgKAFK5djSk",  # Wiz Khalifa See You Again
    ]
    youtube2 = YouTubeAdapter(video_urls=haul_urls_batch2)
    await fetch_and_store(youtube2, limit=100)
    
    # ── 5. WEB REVIEWS / PRODUCT REVIEWS ── More queries across review sites
    web_queries_batch1 = [
        "myntra review site:mouthshut.com",
        "myntra complaint site:consumercomplaints.in",
        "myntra experience site:quora.com",
        "myntra wishlist site:quora.com",
    ]
    web1 = WebReviewsAdapter(queries=web_queries_batch1)
    await fetch_and_store(web1, limit=50)
    
    web_queries_batch2 = [
        "myntra sizing wrong site:quora.com",
        "myntra return policy review",
        "myntra vs amazon fashion review",
        "myntra fake reviews site:reddit.com",
    ]
    web2 = WebReviewsAdapter(queries=web_queries_batch2)
    await fetch_and_store(web2, limit=50)
    
    # ── 6. TWITTER ── Broader search terms
    twitter_queries_batch1 = [
        "myntra",
        "myntra delivery",
        "myntra refund",
        "myntra quality",
    ]
    twitter1 = TwitterAdapter(queries=twitter_queries_batch1)
    await fetch_and_store(twitter1, limit=100)
    
    twitter_queries_batch2 = [
        "myntra sale",
        "myntra exchange",
        "myntra sizing wrong",
        "myntra app",
    ]
    twitter2 = TwitterAdapter(queries=twitter_queries_batch2)
    await fetch_and_store(twitter2, limit=100)
    
    # ── 7. INSTAGRAM ── Use multiple popular Myntra-related posts
    instagram_urls = [
        "https://www.instagram.com/p/C5K7cXyIpVN/",  # Myntra official
        "https://www.instagram.com/p/C4sE3YqIzQv/",  # Myntra fashion
        "https://www.instagram.com/p/C3xR2mWo8zy/",  # Shopping haul
    ]
    instagram1 = InstagramAdapter(reel_urls=instagram_urls)
    await fetch_and_store(instagram1, limit=100)
    
    print("\n🎉 Expanded data fetch complete!")

if __name__ == "__main__":
    asyncio.run(main())
