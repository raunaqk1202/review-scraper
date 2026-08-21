import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.db.session import AsyncSessionLocal as async_session
from app.models.opportunities import Opportunity, OpportunityScore
from sqlalchemy.future import select
import os
# pyrefly: ignore [missing-import]
import instructor
from groq import AsyncGroq
from pydantic import BaseModel, Field

groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)
MODEL_NAME = "openai/gpt-oss-120b"

class OpportunityScoringSchema(BaseModel):
    impact: float = Field(..., description="Impact of the opportunity (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)")
    confidence: float = Field(..., description="Confidence in the opportunity (1.0=high, 0.8=medium, 0.5=low)")
    effort: float = Field(..., description="Effort to implement in person-months (e.g., 0.5, 1.0, 2.0, 3.0)")

async def score_opportunities():
    async with async_session() as db:
        result = await db.execute(select(Opportunity))
        opportunities = result.scalars().all()
        
        if not opportunities:
            print("No opportunities found. Run cluster_signals.py first.")
            return

        # Simple mock total for reach calculation since we are running on a subset
        TOTAL_SIGNALS = 20.0 
            
        print(f"Scoring {len(opportunities)} opportunities...")
        
        for opp in opportunities:
            # 1. Objective Metrics (Reach)
            reach = float(opp.supporting_conversations)
            if reach < 1.0: reach = 1.0 # Minimum reach of 1
            
            # 3. AI-Driven Metrics (Impact, Confidence, Effort)
            print(f"\nScoring: {opp.title}")
            try:
                ai_score = await client.chat.completions.create(
                    model=MODEL_NAME,
                    response_model=OpportunityScoringSchema,
                    messages=[
                        {"role": "system", "content": "You are a product manager estimating RICE scores for ecommerce opportunities. Output impact, confidence, and effort."},
                        {"role": "user", "content": f"Title: {opp.title}\nDesc: {opp.description}\nEvaluate Impact, Confidence, and Effort."}
                    ],
                    temperature=0.0,
                )
                
                # 4. RICE Calculation
                effort = max(ai_score.effort, 0.1) # Prevent division by zero
                composite_score = (reach * ai_score.impact * ai_score.confidence) / effort
                
                print(f"  Reach: {reach:.2f}, Impact: {ai_score.impact:.2f}, Confidence: {ai_score.confidence:.2f}, Effort: {ai_score.effort:.2f}")
                print(f"  --> Final RICE Score: {composite_score:.2f}")
                
                score = OpportunityScore(
                    opportunity_id=opp.id,
                    reach=reach,
                    severity=ai_score.effort, # using severity for effort
                    business_impact=ai_score.impact,
                    evidence_strength=ai_score.confidence,
                    composite_score=composite_score
                )
                db.add(score)
            except Exception as e:
                print(f"Error scoring {opp.title}: {e}")
                
        await db.commit()
        print("\n✅ Quantification & Scoring Complete!")

if __name__ == "__main__":
    asyncio.run(score_opportunities())
