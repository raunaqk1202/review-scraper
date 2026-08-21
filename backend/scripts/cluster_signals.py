import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.db.session import AsyncSessionLocal as async_session
from app.models.signals import AISignal
from app.models.opportunities import Opportunity, OpportunityScore
from sqlalchemy.future import select
from sqlalchemy import delete
import os
# pyrefly: ignore [missing-import]
import instructor
from groq import AsyncGroq
from pydantic import BaseModel, Field
from typing import List

groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)
MODEL_NAME = "openai/gpt-oss-120b"

class OpportunitySchema(BaseModel):
    title: str = Field(..., description="Short catchy title of the opportunity")
    description: str = Field(..., description="Detailed description of the friction or opportunity")
    signal_ids: List[str] = Field(..., description="List of exact AISignal IDs that belong to this opportunity")

class ClusteringResult(BaseModel):
    opportunities: List[OpportunitySchema] = Field(..., description="List of identified opportunities")

async def cluster_signals():
    async with async_session() as db:
        result = await db.execute(select(AISignal))
        signals = result.scalars().all()
        
        if not signals:
            print("No signals found in the database. Run run_pipeline.py first.")
            return

        print(f"Loaded {len(signals)} signals for clustering.")
        
        payload = []
        for s in signals:
            payload.append(f"ID: {s.id}\nJourney Stage: {s.journey_stage}\nBarrier/Signal: {s.summary}\n---")
        
        prompt = "Cluster the following behavioral signals into up to 15 distinct high-impact business opportunities based on the data. Do not artificially limit them if there are many unique themes. For each opportunity, list the exact IDs of the signals that belong to it.\n\n" + "\n".join(payload)

        print("Sending to Groq for clustering...")
        try:
            clustering_result = await client.chat.completions.create(
                model=MODEL_NAME,
                response_model=ClusteringResult,
                messages=[
                    {"role": "system", "content": "You are a Chief Product Officer. Analyze user behavioral signals and group them into major Product Opportunities. CRITICAL INSTRUCTION: In product management, opportunities are unmet customer needs, pain points, or desires that live exclusively in the problem space. Strictly remove ALL solution suggestions from your output. Focus entirely on the 'Why' and 'What': the core customer pain point, unmet need, or desire. Ensure every signal is mapped to an opportunity."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
            )
            
            # Save opportunities to DB
            await db.execute(delete(Opportunity))
            await db.execute(delete(OpportunityScore))
            await db.commit()
            
            for opp in clustering_result.opportunities:
                print(f"\nOpportunity: {opp.title} ({len(opp.signal_ids)} signals)")
                print(f"Desc: {opp.description}")
                new_opp = Opportunity(
                    title=opp.title,
                    description=opp.description,
                    supporting_conversations=len(opp.signal_ids),
                    barrier=opp.description
                )
                db.add(new_opp)
                # Note: We aren't linking back the signal IDs permanently here just to keep the script simple.
                # In a real app we'd update the `opportunity_theme` in `ai_signal`.
                
            await db.commit()
            print("\n✅ Clustering Complete!")
        except Exception as e:
            print(f"Error during clustering: {e}")

if __name__ == "__main__":
    asyncio.run(cluster_signals())
