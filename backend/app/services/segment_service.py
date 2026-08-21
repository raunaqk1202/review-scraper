from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.opportunities import Opportunity

class SegmentService:
    async def compare_segments(self, db: AsyncSession, dimension: str, values: List[str]) -> Dict[str, Any]:
        """
        Compare opportunities across different segments (e.g. user_type).
        """
        result = {}
        for val in values:
            query = select(Opportunity).where(Opportunity.user_segment == val)
            res = await db.execute(query)
            opps = res.scalars().all()
            
            result[val] = {
                "opportunity_count": len(opps),
                "top_barriers": [o.barrier for o in opps[:3] if o.barrier],
                "average_confidence": sum(o.confidence_level for o in opps if o.confidence_level) / len(opps) if opps else 0
            }
            
        return result

segment_service = SegmentService()
