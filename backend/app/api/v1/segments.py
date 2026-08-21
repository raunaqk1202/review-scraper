from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.api.deps import get_db
from app.services.segment_service import segment_service

router = APIRouter()

@router.get("/compare", response_model=Dict[str, Any])
async def compare_segments(
    dimension: str = Query(..., description="Dimension to compare, e.g. user_type"),
    values: List[str] = Query(..., description="Values to compare"),
    db: AsyncSession = Depends(get_db)
):
    """
    Compare barrier/opportunity distributions across segments.
    """
    return await segment_service.compare_segments(db, dimension, values)
