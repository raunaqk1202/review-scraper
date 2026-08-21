import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.opportunities import Opportunity

@pytest.mark.asyncio
async def test_traceability_audit(db_session: AsyncSession):
    # Fetch all opportunities with their evidence chain
    query = select(Opportunity).options(
        selectinload(Opportunity.evidences)
    )
    result = await db_session.execute(query)
    opportunities = result.scalars().all()
    
    for opp in opportunities:
        # 100% of opportunities must have a complete evidence chain
        assert len(opp.evidences) > 0, f"Opportunity {opp.id} has no evidence"
        
        for ev in opp.evidences:
            # Evidence must link back to a pattern
            assert ev.pattern_id is not None, f"Evidence {ev.id} is an orphan with no pattern"
