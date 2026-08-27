"""Re-score all existing opportunities using the Groq LLM.

Formula: Score = 35% × User Pain + 30% × Business Impact + 20% × Reach + 15% × Evidence Strength
Composite = 7×Pain + 6×Impact + 4×Reach + 3×Evidence (0–100 scale)

Usage:
    cd backend && source .venv/bin/activate
    python scripts/rescore_opportunities.py
"""
import os
import sys
import sqlite3
import uuid
import asyncio
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import instructor
from groq import AsyncGroq
from app.services.schemas import OpportunityScoringResult

# LLM setup
groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)
MODEL_NAME = os.environ.get("GROQ_MODEL", "qwen/qwen3.6-27b")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "discovery_engine.db")

SCORING_WEIGHTS = {"user_pain": 7, "business_impact": 6, "reach": 4, "evidence_strength": 3}

SCORING_PROMPT = """You are an expert product analyst scoring opportunity areas for Myntra, a fashion e-commerce platform.

Rate each dimension from 1.0 to 5.0 based on the evidence provided:

- user_pain: How severe is this problem for users? 1=minor inconvenience, 5=critical blocker preventing purchase.
- business_impact: How much could solving this affect conversion/revenue/retention? 1=negligible, 5=major revenue driver.
- reach: How widespread is this problem across the user base? Consider the number of supporting conversations and source platforms. 1=very niche, 5=affects most users.
- evidence_strength: How confident are we in this finding? Consider independent sources, cross-platform consistency. 1=single anecdotal mention, 5=consistent pattern across multiple sources.

Be rigorous and evidence-based. Do not inflate scores."""


async def score_one(title, description, barrier, supporting_convs, independent_sources, evidence_level):
    context = f"""Opportunity: {title}
Description: {description or 'N/A'}
Barrier: {barrier or 'N/A'}
Supporting Conversations: {supporting_convs}
Independent Sources: {independent_sources}
Evidence Level: {evidence_level or 'N/A'}"""

    return await client.chat.completions.create(
        model=MODEL_NAME,
        response_model=OpportunityScoringResult,
        messages=[
            {"role": "system", "content": SCORING_PROMPT},
            {"role": "user", "content": context}
        ],
        temperature=0.1,
    )


async def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Load all opportunities
    cursor.execute("""
        SELECT id, title, description, barrier, unmet_need, 
               supporting_conversations, independent_sources, evidence_level
        FROM opportunity
    """)
    opportunities = cursor.fetchall()
    print(f"Found {len(opportunities)} opportunities to re-score\n")
    
    weights_json = str(SCORING_WEIGHTS).replace("'", '"')
    now = datetime.utcnow().isoformat()
    
    for opp in opportunities:
        opp_id = opp["id"]
        title = opp["title"]
        
        try:
            scores = await score_one(
                title=title,
                description=opp["description"],
                barrier=opp["barrier"],
                supporting_convs=opp["supporting_conversations"] or 0,
                independent_sources=opp["independent_sources"] or 0,
                evidence_level=opp["evidence_level"]
            )
            
            composite = (
                SCORING_WEIGHTS["user_pain"] * scores.user_pain +
                SCORING_WEIGHTS["business_impact"] * scores.business_impact +
                SCORING_WEIGHTS["reach"] * scores.reach +
                SCORING_WEIGHTS["evidence_strength"] * scores.evidence_strength
            )
            
            # Upsert: delete existing score and insert new one
            cursor.execute("DELETE FROM opportunity_score WHERE opportunity_id = ?", (opp_id,))
            cursor.execute(
                """INSERT INTO opportunity_score 
                   (id, opportunity_id, user_pain, business_impact, reach, evidence_strength, 
                    composite_score, dimension_weights, scored_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (str(uuid.uuid4()), opp_id,
                 scores.user_pain, scores.business_impact, scores.reach, scores.evidence_strength,
                 composite, weights_json, now)
            )
            conn.commit()
            
            print(f"✅ {title}")
            print(f"   Pain={scores.user_pain:.1f}  Impact={scores.business_impact:.1f}  "
                  f"Reach={scores.reach:.1f}  Evidence={scores.evidence_strength:.1f}  "
                  f"→ Composite={composite:.1f}/100\n")
                  
        except Exception as e:
            print(f"❌ {title}: {e}\n")
    
    # Print final summary
    cursor.execute("""
        SELECT o.title, os.user_pain, os.business_impact, os.reach, os.evidence_strength, os.composite_score
        FROM opportunity o 
        JOIN opportunity_score os ON o.id = os.opportunity_id
        ORDER BY os.composite_score DESC
    """)
    rows = cursor.fetchall()
    
    print("\n" + "="*90)
    print(f"{'Rank':<5} {'Title':<50} {'Pain':>5} {'Imp':>5} {'Reach':>5} {'Evid':>5} {'Score':>7}")
    print("="*90)
    for i, row in enumerate(rows, 1):
        print(f"{i:<5} {row[0][:48]:<50} {row[1]:>5.1f} {row[2]:>5.1f} {row[3]:>5.1f} {row[4]:>5.1f} {row[5]:>7.1f}")
    print("="*90)
    
    conn.close()


if __name__ == "__main__":
    asyncio.run(main())
