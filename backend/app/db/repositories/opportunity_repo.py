from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.opportunities import Opportunity, OpportunityScore
from app.db.repositories.base_repo import BaseRepository

class OpportunityRepository(BaseRepository):
    def __init__(self):
        super().__init__(Opportunity)

    async def get_with_score(self, db: AsyncSession, id: str) -> Optional[Opportunity]:
        result = await db.execute(
            select(Opportunity)
            .options(selectinload(Opportunity.score))
            .filter(Opportunity.id == id)
        )
        return result.scalars().first()

    async def get_top_opportunities(self, db: AsyncSession, limit: int = 10) -> List[Opportunity]:
        result = await db.execute(
            select(Opportunity)
            .join(OpportunityScore)
            .options(selectinload(Opportunity.score))
            .order_by(OpportunityScore.composite_score.desc())
            .limit(limit)
        )
        return result.scalars().all()

opportunity_repo = OpportunityRepository()
