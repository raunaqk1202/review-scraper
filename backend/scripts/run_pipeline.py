import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.db.session import AsyncSessionLocal as async_session
from app.db.repositories.feedback_repo import feedback_repo
from app.services.llm_pipeline import filter_noise, extract_signals
from app.models.signals import AISignal
from sqlalchemy.future import select
from datetime import datetime

async def process_feedback_items():
    async with async_session() as db:
        # Process all platforms
        query = (
            select(feedback_repo.model)
            .where(feedback_repo.model.processed_at == None)
        )
        result = await db.execute(query)
        unprocessed_items = result.scalars().all()
        
        print(f"Found {len(unprocessed_items)} unprocessed feedback items.")
        
        for item in unprocessed_items:
            text = item.original_text
            print(f"\nProcessing Item ID: {item.id}")
            print(f"Text Snippet: {text[:100]}...")
            
            # Stage 1: Noise Reduction
            try:
                noise_result = await filter_noise(text)
                print(f"  -> Relevant? {noise_result.is_relevant} (Reason: {noise_result.reason})")
            except Exception as e:
                print(f"  -> Error in Noise Reduction: {e}")
                continue
                
            if not noise_result.is_relevant:
                item.processed_at = datetime.utcnow()
                item.is_spam = True
                await db.commit()
                continue
                
            # Stage 2: Signal Extraction
            try:
                extraction = await extract_signals(text)
                print(f"  -> Extracted {len(extraction.signals)} signals.")
                for sig in extraction.signals:
                    print(f"     * [{sig.signal_type}] {sig.summary} (Stage: {sig.journey_stage.value})")
                    
                    new_signal = AISignal(
                        feedback_item_id=item.id,
                        signal_type=sig.signal_type,
                        summary=sig.summary,
                        journey_stage=sig.journey_stage.value,
                        evidence_quote=sig.evidence_quote,
                        confidence_score=0.9 # Base confidence
                    )
                    db.add(new_signal)
            except Exception as e:
                print(f"  -> Error in Signal Extraction: {e}")
                
            item.processed_at = datetime.utcnow()
            await db.commit()
            
    print("\n✅ Pipeline execution complete!")

if __name__ == "__main__":
    asyncio.run(process_feedback_items())
