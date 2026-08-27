import uuid
import os
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import instructor
from groq import AsyncGroq

from app.pipeline.base import PipelineStage
from app.models.patterns import Pattern
from app.models.opportunities import Opportunity, OpportunityScore, OpportunityEvidence
from app.services.schemas import OpportunityScoringResult

# Initialize LLM client for scoring
groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)
MODEL_NAME = os.environ.get("GROQ_MODEL", "qwen/qwen3.6-27b")

SCORING_SYSTEM_PROMPT = """You are an expert product analyst scoring opportunity areas for Myntra, a fashion e-commerce platform.

Rate each dimension from 1.0 to 5.0 based on the evidence provided:

- user_pain: How severe is this problem for users? 1=minor inconvenience, 5=critical blocker preventing purchase.
- business_impact: How much could solving this affect conversion/revenue/retention? 1=negligible, 5=major revenue driver.
- reach: How widespread is this problem across the user base? Consider the number of supporting conversations and whether it appears across multiple platforms. 1=very niche, 5=affects most users.
- evidence_strength: How confident are we in this finding? Consider the number of independent sources, cross-platform consistency, and evidence level. 1=single anecdotal mention, 5=consistent pattern across multiple sources.

Be rigorous and evidence-based. Do not inflate scores."""


async def score_opportunity_with_llm(opportunity: Opportunity) -> OpportunityScoringResult:
    """Score an opportunity using the Groq LLM."""
    context = f"""Opportunity: {opportunity.title}
Description: {opportunity.description or 'N/A'}
Barrier: {opportunity.barrier or 'N/A'}
Unmet Need: {opportunity.unmet_need or 'N/A'}
Supporting Conversations: {opportunity.supporting_conversations}
Independent Sources: {opportunity.independent_sources}
Evidence Level: {opportunity.evidence_level or 'N/A'}"""

    return await client.chat.completions.create(
        model=MODEL_NAME,
        response_model=OpportunityScoringResult,
        messages=[
            {"role": "system", "content": SCORING_SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ],
        temperature=0.1,
    )


class Stage5Opportunities(PipelineStage):
    @property
    def stage_name(self) -> str:
        return "Opportunity Generation"
        
    @property
    def stage_number(self) -> int:
        return 5

    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        self.logger.info("Starting Stage 5: Opportunity Generation & Scoring")
        
        # Load patterns that don't have opportunities yet
        query = select(Pattern).options(selectinload(Pattern.opportunity_evidences))
        result = await db.execute(query)
        patterns = result.scalars().all()
        
        metrics = {
            "patterns_analyzed": len(patterns),
            "opportunities_generated": 0,
            "opportunities_scored": 0
        }
        
        for pattern in patterns:
            # Check if this pattern is already linked to an opportunity
            if len(pattern.opportunity_evidences) > 0:
                continue
                
            opp_id = str(uuid.uuid4())
            
            opp = Opportunity(
                id=opp_id,
                title=f"Opportunity from {pattern.name}",
                description="Auto-generated opportunity based on extracted behavioral patterns.",
                user_segment="General",
                context="General Context",
                behavior="Observed recurring behavior",
                barrier="Identified barrier",
                unmet_need="Unmet need",
                potential_solution="Suggested solution",
                potential_business_impact="Medium Impact",
                evidence_level="HYPOTHESIZED",
                supporting_conversations=pattern.occurrence_count,
                independent_sources=1,
                confidence_level=0.75
            )
            db.add(opp)
            metrics["opportunities_generated"] += 1
            
            # Score using LLM
            try:
                llm_scores = await score_opportunity_with_llm(opp)
                composite = OpportunityScore.compute_composite_score(
                    user_pain=llm_scores.user_pain,
                    business_impact=llm_scores.business_impact,
                    reach=llm_scores.reach,
                    evidence_strength=llm_scores.evidence_strength
                )
                
                score = OpportunityScore(
                    id=str(uuid.uuid4()),
                    opportunity_id=opp_id,
                    user_pain=llm_scores.user_pain,
                    business_impact=llm_scores.business_impact,
                    reach=llm_scores.reach,
                    evidence_strength=llm_scores.evidence_strength,
                    composite_score=composite,
                    dimension_weights=OpportunityScore.SCORING_WEIGHTS,
                )
                db.add(score)
                metrics["opportunities_scored"] += 1
                self.logger.info(f"Scored '{opp.title}': {composite:.1f}/100")
            except Exception as e:
                self.logger.warning(f"LLM scoring failed for '{opp.title}': {e}. Using fallback.")
                # Fallback: conservative default scores
                score = OpportunityScore(
                    id=str(uuid.uuid4()),
                    opportunity_id=opp_id,
                    user_pain=3.0,
                    business_impact=3.0,
                    reach=2.0,
                    evidence_strength=2.0,
                    composite_score=OpportunityScore.compute_composite_score(3.0, 3.0, 2.0, 2.0),
                    dimension_weights=OpportunityScore.SCORING_WEIGHTS,
                )
                db.add(score)
            
            # Evidence
            evidence = OpportunityEvidence(
                opportunity_id=opp_id,
                pattern_id=pattern.id,
                evidence_type="PATTERN",
                evidence_level="DERIVED",
                evidence_text=f"Derived from pattern {pattern.name}"
            )
            db.add(evidence)
            
        await db.commit()
        return metrics
