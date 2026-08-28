# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any

from app.api.deps import get_db
from app.models.opportunities import Opportunity, OpportunityScore
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

@router.post("/rescore_all", response_model=Dict[str, Any])
async def rescore_all_opportunities(db: AsyncSession = Depends(get_db)):
    """Re-score all existing opportunities using the LLM (useful for production migrations)."""
    from app.pipeline.stage_5_opportunities import score_opportunity_with_llm
    from app.models.opportunities import OpportunityScore
    import uuid
    
    query = select(Opportunity).options(selectinload(Opportunity.score))
    result = await db.execute(query)
    opportunities = result.scalars().all()
    
    scored_count = 0
    errors = []
    
    for opp in opportunities:
        try:
            llm_scores = await score_opportunity_with_llm(opp)
            
            composite = OpportunityScore.compute_composite_score(
                user_pain=llm_scores.user_pain,
                business_impact=llm_scores.business_impact,
                reach=llm_scores.reach,
                evidence_strength=llm_scores.evidence_strength
            )
            
            if opp.score:
                # Update existing score
                opp.score.user_pain = llm_scores.user_pain
                opp.score.business_impact = llm_scores.business_impact
                opp.score.reach = llm_scores.reach
                opp.score.evidence_strength = llm_scores.evidence_strength
                opp.score.composite_score = composite
                opp.score.dimension_weights = OpportunityScore.SCORING_WEIGHTS
            else:
                # Create new score
                new_score = OpportunityScore(
                    id=str(uuid.uuid4()),
                    opportunity_id=opp.id,
                    user_pain=llm_scores.user_pain,
                    business_impact=llm_scores.business_impact,
                    reach=llm_scores.reach,
                    evidence_strength=llm_scores.evidence_strength,
                    composite_score=composite,
                    dimension_weights=OpportunityScore.SCORING_WEIGHTS,
                )
                db.add(new_score)
            
            scored_count += 1
        except Exception as e:
            errors.append(f"Failed to score {opp.title}: {str(e)}")
            
    await db.commit()
    
    return {
        "status": "success",
        "scored_count": scored_count,
        "errors": errors
    }


from pydantic import BaseModel

class ScoreSyncItem(BaseModel):
    title: str
    user_pain: float
    business_impact: float
    reach: float
    evidence_strength: float

@router.patch("/sync_scores", response_model=Dict[str, Any])
async def sync_scores(scores: List[ScoreSyncItem], db: AsyncSession = Depends(get_db)):
    """Directly set opportunity scores from provided values (no LLM call).
    
    Each item should have: title, user_pain, business_impact, reach, evidence_strength.
    Composite score is recalculated using the standard formula.
    """
    import uuid
    
    try:
        query = select(Opportunity).options(selectinload(Opportunity.score))
        result = await db.execute(query)
        opportunities = result.scalars().all()
        
        # Build lookup by title
        opp_map = {opp.title: opp for opp in opportunities}
        
        updated = 0
        errors = []
        
        for item in scores:
            title = item.title
            if title not in opp_map:
                errors.append(f"Opportunity not found: {title}")
                continue
            
            opp = opp_map[title]
            
            composite = OpportunityScore.compute_composite_score(
                user_pain=item.user_pain,
                business_impact=item.business_impact,
                reach=item.reach,
                evidence_strength=item.evidence_strength
            )
            
            if opp.score:
                opp.score.user_pain = item.user_pain
                opp.score.business_impact = item.business_impact
                opp.score.reach = item.reach
                opp.score.evidence_strength = item.evidence_strength
                opp.score.composite_score = composite
                opp.score.dimension_weights = OpportunityScore.SCORING_WEIGHTS
            else:
                new_score = OpportunityScore(
                    id=str(uuid.uuid4()),
                    opportunity_id=opp.id,
                    user_pain=item.user_pain,
                    business_impact=item.business_impact,
                    reach=item.reach,
                    evidence_strength=item.evidence_strength,
                    composite_score=composite,
                    dimension_weights=OpportunityScore.SCORING_WEIGHTS,
                )
                db.add(new_score)
            
            updated += 1
        
        await db.commit()
        
        return {
            "status": "success",
            "updated_count": updated,
            "errors": errors
        }
    except Exception as e:
        return {
            "status": "error",
            "updated_count": 0,
            "errors": [str(e)]
        }
