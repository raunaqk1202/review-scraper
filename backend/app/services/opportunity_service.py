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
        # For MVP we will just update all scores in the DB to reflect new weights
        # In a real app we'd trigger a background job to recalculate
        query = select(OpportunityScore)
        result = await db.execute(query)
        scores = result.scalars().all()
        
        for score in scores:
            score.dimension_weights = weights
            # Recalculate composite based on weights (default to 1.0 for each if not specified)
            w_reach = weights.get("reach", 1.0)
            w_sev = weights.get("severity", 1.0)
            w_bus = weights.get("business_impact", 1.0)
            
            # Simple weighted average
            total_weight = w_reach + w_sev + w_bus
            if total_weight > 0:
                score.composite_score = (
                    (score.reach * w_reach) + 
                    (score.severity * w_sev) + 
                    (score.business_impact * w_bus)
                ) / total_weight
                
        await db.commit()
        return True

opportunity_service = OpportunityService()
