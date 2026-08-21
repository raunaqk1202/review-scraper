from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.repositories.feedback_repo import feedback_repo
from app.models.feedback import DataSource, FeedbackItem
from app.ingestion.playstore_adapter import PlayStoreAdapter
from app.ingestion.appstore_adapter import AppStoreAdapter
from app.ingestion.reddit_adapter import RedditAdapter
from app.ingestion.youtube_adapter import YouTubeAdapter
from app.ingestion.twitter_adapter import TwitterAdapter
from app.ingestion.instagram_adapter import InstagramAdapter
from app.ingestion.web_reviews_adapter import WebReviewsAdapter
from app.models.enums import SourcePlatform

class IngestionService:
    @staticmethod
    def get_adapter(platform: str, **kwargs):
        if platform == SourcePlatform.PLAY_STORE.value:
            return PlayStoreAdapter(**kwargs)
        elif platform == SourcePlatform.APP_STORE.value:
            return AppStoreAdapter(**kwargs)
        elif platform == SourcePlatform.REDDIT.value:
            return RedditAdapter(**kwargs)
        elif platform == SourcePlatform.YOUTUBE.value:
            return YouTubeAdapter(**kwargs)
        elif platform == SourcePlatform.TWITTER.value:
            return TwitterAdapter(**kwargs)
        elif platform == SourcePlatform.INSTAGRAM.value:
            return InstagramAdapter(**kwargs)
        elif platform == "WEB_REVIEWS":
            return WebReviewsAdapter(**kwargs)
        else:
            raise ValueError(f"Unknown platform: {platform}")

    @staticmethod
    async def get_or_create_datasource(db: AsyncSession, platform: str) -> str:
        result = await db.execute(select(DataSource).filter(DataSource.platform == platform))
        ds = result.scalars().first()
        if not ds:
            ds = DataSource(platform=platform, source_type="api", description=f"Real data from {platform}")
            db.add(ds)
            await db.commit()
            await db.refresh(ds)
        return ds.id

    @staticmethod
    async def ingest_from_source(db: AsyncSession, platform: str, limit: int = 50, **kwargs) -> Dict[str, Any]:
        adapter = IngestionService.get_adapter(platform, **kwargs)
        raw_data = await adapter.fetch(limit=limit)
        normalized = adapter.normalize(raw_data)
        
        source_id = await IngestionService.get_or_create_datasource(db, adapter.platform_name)
        
        new_items = 0
        duplicate_items = 0
        
        for item in normalized:
            item["source_id"] = source_id
            existing = await feedback_repo.get_by_hash(db, item["content_hash"])
            if not existing:
                await feedback_repo.create(db, obj_in=item)
                new_items += 1
            else:
                duplicate_items += 1
                
        return {
            "platform": platform,
            "fetched": len(normalized),
            "new_items_stored": new_items,
            "duplicates_skipped": duplicate_items
        }

ingestion_service = IngestionService()
