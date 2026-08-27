# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any

from app.api.deps import get_db
from app.models.opportunities import Opportunity
from app.schemas.opportunity import OpportunityResponse
from app.services.opportunity_service import opportunity_service
from app.services.evidence_service import evidence_service

router = APIRouter()

@router.get("", response_model=List[OpportunityResponse])
async def list_opportunities(db: AsyncSession = Depends(get_db)):
    """Fetch all calculated opportunities, ordered by ROI composite score."""
    query = select(Opportunity).options(selectinload(Opportunity.score))
    result = await db.execute(query)
    opportunities = result.scalars().all()
    
    opportunities = sorted(
        opportunities, 
        key=lambda o: o.score.composite_score if o.score else 0.0, 
        reverse=True
    )
    
    return opportunities

@router.get("/{id}", response_model=Dict[str, Any])
async def get_opportunity(id: str, db: AsyncSession = Depends(get_db)):
    """Full opportunity detail with score breakdown."""
    opp = await opportunity_service.get_opportunity(db, id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    score_data = None
    if opp.score:
        score_data = {
            "user_pain": opp.score.user_pain,
            "business_impact": opp.score.business_impact,
            "reach": opp.score.reach,
            "evidence_strength": opp.score.evidence_strength,
            "composite_score": opp.score.composite_score,
            "formula": "Score = 35% × User Pain + 30% × Business Impact + 20% × Reach + 15% × Evidence Strength",
            "dimension_weights": opp.score.dimension_weights,
        }
    
    return {
        "id": opp.id,
        "title": opp.title,
        "description": opp.description,
        "user_segment": opp.user_segment,
        "barrier": opp.barrier,
        "unmet_need": opp.unmet_need,
        "supporting_conversations": opp.supporting_conversations,
        "score": score_data,
    }

@router.get("/{id}/evidence", response_model=List[Dict[str, Any]])
async def get_opportunity_evidence(id: str, db: AsyncSession = Depends(get_db)):
    """Drill-down: linked patterns, clusters, feedback items."""
    evidence_chain = await evidence_service.get_opportunity_drilldown(db, id)
    return evidence_chain

@router.put("/score/weights", response_model=Dict[str, Any])
async def update_score_weights(weights: Dict[str, float], db: AsyncSession = Depends(get_db)):
    """Update scoring weights -> re-calculate composite scores."""
    await opportunity_service.update_score_weights(db, weights)
    return {"status": "success", "message": "Weights updated"}
