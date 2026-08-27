from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.opportunities import Opportunity, OpportunityScore

class OpportunityService:
    async def get_opportunity(self, db: AsyncSession, opp_id: str) -> Opportunity:
        query = select(Opportunity).where(Opportunity.id == opp_id).options(
            selectinload(Opportunity.score),
            selectinload(Opportunity.evidences)
        )
        result = await db.execute(query)
        return result.scalars().first()
        
    async def update_score_weights(self, db: AsyncSession, weights: Dict[str, float]) -> bool:
        """Recalculate composite scores using custom dimension weights.
        
        Weights dict example: {"user_pain": 7, "business_impact": 6, "reach": 4, "evidence_strength": 3}
        """
        query = select(OpportunityScore)
        result = await db.execute(query)
        scores = result.scalars().all()
        
        for score in scores:
            score.dimension_weights = weights
            
            w_pain = weights.get("user_pain", 7)
            w_impact = weights.get("business_impact", 6)
            w_reach = weights.get("reach", 4)
            w_evidence = weights.get("evidence_strength", 3)
            
            score.composite_score = (
                w_pain * (score.user_pain or 3.0) +
                w_impact * (score.business_impact or 3.0) +
                w_reach * (score.reach or 2.0) +
                w_evidence * (score.evidence_strength or 2.0)
            )
                
        await db.commit()
        return True

opportunity_service = OpportunityService()
