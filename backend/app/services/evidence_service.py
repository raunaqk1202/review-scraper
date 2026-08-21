from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.feedback import FeedbackItem
from app.models.clusters import Cluster
from app.models.patterns import Pattern
from app.models.opportunities import OpportunityEvidence

class EvidenceService:
    async def get_feedback(self, db: AsyncSession, item_id: str) -> FeedbackItem:
        query = select(FeedbackItem).where(FeedbackItem.id == item_id).options(
            selectinload(FeedbackItem.source),
            selectinload(FeedbackItem.signals)
        )
        result = await db.execute(query)
        return result.scalars().first()
        
    async def get_cluster(self, db: AsyncSession, cluster_id: str) -> Cluster:
        query = select(Cluster).where(Cluster.id == cluster_id).options(
            selectinload(Cluster.memberships).selectinload(lambda m: m.feedback_item)
        )
        result = await db.execute(query)
        return result.scalars().first()
        
    async def get_pattern(self, db: AsyncSession, pattern_id: str) -> Pattern:
        query = select(Pattern).where(Pattern.id == pattern_id).options(
            selectinload(Pattern.opportunity_evidences)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_opportunity_drilldown(self, db: AsyncSession, opportunity_id: str) -> List[Dict[str, Any]]:
        # Returns the evidence chain
        query = select(OpportunityEvidence).where(OpportunityEvidence.opportunity_id == opportunity_id).options(
            selectinload(OpportunityEvidence.pattern).selectinload(Pattern.opportunity_evidences)
        )
        result = await db.execute(query)
        evidences = result.scalars().all()
        
        chain = []
        for ev in evidences:
            chain.append({
                "evidence_id": ev.id,
                "type": ev.evidence_type,
                "text": ev.evidence_text,
                "pattern": {
                    "id": ev.pattern.id,
                    "name": ev.pattern.name
                } if ev.pattern else None
            })
        return chain

evidence_service = EvidenceService()
