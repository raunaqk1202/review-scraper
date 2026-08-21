from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.api.deps import get_db
from app.services.evidence_service import evidence_service

router = APIRouter()

@router.get("/drilldown", response_model=List[Dict[str, Any]])
async def get_opportunity_drilldown(opportunity_id: str, db: AsyncSession = Depends(get_db)):
    """Full chain: Opportunity -> Pattern -> Cluster -> Feedback -> Source."""
    return await evidence_service.get_opportunity_drilldown(db, opportunity_id)

@router.get("/feedback/{id}", response_model=Dict[str, Any])
async def get_feedback(id: str, db: AsyncSession = Depends(get_db)):
    """Original feedback with source metadata."""
    item = await evidence_service.get_feedback(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Feedback item not found")
        
    return {
        "id": item.id,
        "original_text": item.original_text,
        "cleaned_text": item.cleaned_text,
        "source_platform": item.source_platform,
        "is_spam": item.is_spam
    }

@router.get("/cluster/{id}", response_model=Dict[str, Any])
async def get_cluster(id: str, db: AsyncSession = Depends(get_db)):
    """Cluster detail + member list."""
    cluster = await evidence_service.get_cluster(db, id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
        
    return {
        "id": cluster.id,
        "label": cluster.label,
        "member_count": cluster.member_count,
        "members": [{"item_id": m.feedback_item_id, "score": m.similarity_score} for m in cluster.memberships]
    }

@router.get("/pattern/{id}", response_model=Dict[str, Any])
async def get_pattern(id: str, db: AsyncSession = Depends(get_db)):
    """Pattern detail with supporting evidence."""
    pattern = await evidence_service.get_pattern(db, id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
        
    return {
        "id": pattern.id,
        "name": pattern.name,
        "pattern_type": pattern.pattern_type,
        "occurrence_count": pattern.occurrence_count
    }
