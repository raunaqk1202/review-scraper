from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any

from app.api.deps import get_db
from app.models.patterns import Pattern

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
async def get_trends(db: AsyncSession = Depends(get_db)):
    """
    Trend analysis for patterns.
    """
    query = select(Pattern)
    result = await db.execute(query)
    patterns = result.scalars().all()
    
    return [
        {
            "pattern_id": p.id,
            "name": p.name,
            "trend_direction": p.trend_direction,
            "occurrence_count": p.occurrence_count
        }
        for p in patterns
    ]
