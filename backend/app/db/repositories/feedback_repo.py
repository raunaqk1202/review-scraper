from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.feedback import FeedbackItem, DataSource
from app.db.repositories.base_repo import BaseRepository

class FeedbackRepository(BaseRepository):
    def __init__(self):
        super().__init__(FeedbackItem)

    async def get_by_hash(self, db: AsyncSession, content_hash: str) -> Optional[FeedbackItem]:
        result = await db.execute(
            select(FeedbackItem).filter(FeedbackItem.content_hash == content_hash)
        )
        return result.scalars().first()

    async def bulk_create(self, db: AsyncSession, items: List[dict]) -> List[FeedbackItem]:
        db_objs = [FeedbackItem(**item) for item in items]
        db.add_all(db_objs)
        await db.commit()
        return db_objs

    async def list_unprocessed(self, db: AsyncSession, limit: int = 50) -> List[FeedbackItem]:
        result = await db.execute(
            select(FeedbackItem)
            .filter(FeedbackItem.processed_at.is_(None))
            .filter(FeedbackItem.is_spam == False)
            .filter(FeedbackItem.is_duplicate == False)
            .limit(limit)
        )
        return result.scalars().all()

feedback_repo = FeedbackRepository()
