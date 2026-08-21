import uuid
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.pipeline.base import PipelineStage
from app.models.clusters import Cluster
from app.models.patterns import Pattern, PatternEvidence

class Stage4Patterns(PipelineStage):
    @property
    def stage_name(self) -> str:
        return "Pattern Detection"
        
    @property
    def stage_number(self) -> int:
        return 4

    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        self.logger.info("Starting Stage 4: Pattern Detection")
        
        # In this MVP stage, we will turn Clusters into Patterns
        # if they have more than 3 occurrences.
        query = select(Cluster).options(selectinload(Cluster.memberships))
        result = await db.execute(query)
        clusters = result.scalars().all()
        
        metrics = {
            "clusters_analyzed": len(clusters),
            "patterns_detected": 0
        }
        
        for cluster in clusters:
            if cluster.member_count >= 3:
                pattern = Pattern(
                    id=str(uuid.uuid4()),
                    name=f"Pattern from {cluster.label}",
                    pattern_type="BEHAVIORAL",
                    evidence_level="DERIVED",
                    occurrence_count=cluster.member_count,
                    trend_direction="STABLE"
                )
                db.add(pattern)
                
                # Add evidence
                for membership in cluster.memberships:
                    evidence = PatternEvidence(
                        pattern_id=pattern.id,
                        cluster_id=cluster.id,
                        feedback_item_id=membership.feedback_item_id,
                        evidence_type="CLUSTER_MEMBER"
                    )
                    db.add(evidence)
                    
                metrics["patterns_detected"] += 1
                
        await db.commit()
        return metrics
