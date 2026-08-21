from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.opportunities import OpportunityEvidence
from app.db.repositories.base_repo import BaseRepository

class EvidenceRepository(BaseRepository):
    def __init__(self):
        super().__init__(OpportunityEvidence)

    async def get_for_opportunity(self, db: AsyncSession, opportunity_id: str) -> List[OpportunityEvidence]:
        result = await db.execute(
            select(OpportunityEvidence)
            .filter(OpportunityEvidence.opportunity_id == opportunity_id)
        )
        return result.scalars().all()

evidence_repo = EvidenceRepository()
