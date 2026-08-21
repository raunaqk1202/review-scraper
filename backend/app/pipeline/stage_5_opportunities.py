import uuid
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.pipeline.base import PipelineStage
from app.models.patterns import Pattern
from app.models.opportunities import Opportunity, OpportunityScore, OpportunityEvidence

class Stage5Opportunities(PipelineStage):
    @property
    def stage_name(self) -> str:
        return "Opportunity Generation"
        
    @property
    def stage_number(self) -> int:
        return 5

    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        self.logger.info("Starting Stage 5: Opportunity Generation")
        
        # Load patterns that don't have opportunities yet
        # For MVP we will just generate one opportunity per pattern
        query = select(Pattern).options(selectinload(Pattern.opportunity_evidences))
        result = await db.execute(query)
        patterns = result.scalars().all()
        
        metrics = {
            "patterns_analyzed": len(patterns),
            "opportunities_generated": 0
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
            
            # Score
            score = OpportunityScore(
                id=str(uuid.uuid4()),
                opportunity_id=opp_id,
                reach=opp.supporting_conversations,
                frequency=0.5,
                severity=1.0, # Effort
                business_impact=3.0, # Impact
                evidence_strength=1.0, # Confidence
                cross_source_consistency=0.5,
                cross_segment_relevance=0.5,
                trend_score=0.5,
                strategic_relevance=0.5,
                composite_score=(opp.supporting_conversations * 3.0 * 1.0) / 1.0, # RICE
                dimension_weights={}
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
            
            metrics["opportunities_generated"] += 1
            
        await db.commit()
        return metrics
