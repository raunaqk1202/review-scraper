import re
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.pipeline.base import PipelineStage
from app.models.feedback import FeedbackItem

class Stage1Cleaning(PipelineStage):
    @property
    def stage_name(self) -> str:
        return "Cleaning & Deduplication"
        
    @property
    def stage_number(self) -> int:
        return 1
        
    def _is_spam(self, text: str) -> bool:
        # Basic rule-based spam detection
        # Check for multiple URLs
        url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        if url_count >= 2:
            return True
        # Check for promotional keywords
        promo_words = ["click here", "buy now", "discount code", "promo code"]
        if any(word in text.lower() for word in promo_words):
            return True
        return False
        
    def _clean_text(self, text: str) -> str:
        # Strip whitespace and weird characters
        cleaned = re.sub(r'\s+', ' ', text).strip()
        return cleaned

    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        self.logger.info("Starting Stage 1: Cleaning & Deduplication")
        
        # Get unprocessed items
        query = select(FeedbackItem).where(FeedbackItem.processed_at == None)
        result = await db.execute(query)
        items = result.scalars().all()
        
        metrics = {
            "items_processed": len(items),
            "spam_flagged": 0,
            "cleaned": 0
        }
        
        for item in items:
            text = item.original_text
            
            if self._is_spam(text):
                item.is_spam = True
                metrics["spam_flagged"] += 1
            else:
                item.cleaned_text = self._clean_text(text)
                metrics["cleaned"] += 1
                
        await db.commit()
        return metrics

# Register with orchestrator below or when importing
