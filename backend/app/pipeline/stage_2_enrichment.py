from typing import Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.pipeline.base import PipelineStage
from app.models.feedback import FeedbackItem
from app.models.signals import AISignal
from app.services.llm_pipeline import extract_signals

class Stage2Enrichment(PipelineStage):
    @property
    def stage_name(self) -> str:
        return "Semantic Enrichment"
        
    @property
    def stage_number(self) -> int:
        return 2

    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        self.logger.info("Starting Stage 2: Semantic Enrichment")
        
        # Get items that are not spam, have been cleaned, and are not fully processed yet
        query = select(FeedbackItem).where(
            FeedbackItem.is_spam == False,
            FeedbackItem.cleaned_text != None,
            FeedbackItem.processed_at == None
        )
        result = await db.execute(query)
        items = result.scalars().all()
        
        metrics = {
            "items_enriched": 0,
            "signals_extracted": 0,
            "errors": 0
        }
        
        for item in items:
            try:
                extraction = await extract_signals(item.cleaned_text)
                
                for sig in extraction.signals:
                    new_signal = AISignal(
                        source_item_id=item.id,
                        signal_type=sig.signal_type,
                        summary=sig.summary,
                        journey_stage=sig.journey_stage.value,
                        evidence_quote=sig.evidence_quote,
                        confidence_score=0.9,
                        evidence_level="OBSERVED"
                    )
                    db.add(new_signal)
                    metrics["signals_extracted"] += 1
                
                # Mark item as fully processed
                item.processed_at = datetime.utcnow()
                metrics["items_enriched"] += 1
                
            except Exception as e:
                self.logger.error(f"Error enriching item {item.id}: {e}")
                metrics["errors"] += 1
                
        await db.commit()
        return metrics
