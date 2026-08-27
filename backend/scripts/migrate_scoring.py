"""Recreate opportunity_score with new scoring dimensions

Replaces 9 unused columns with 4 meaningful dimensions:
user_pain, business_impact, reach, evidence_strength (each 1.0-5.0)
composite_score is now 0-100.

Formula: Score = 35% × User Pain + 30% × Business Impact + 20% × Reach + 15% × Evidence Strength
"""
import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "discovery_engine.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Migrating: {DB_PATH}")
    
    # 1. Backup existing opportunity_score data
    cursor.execute("SELECT opportunity_id FROM opportunity_score")
    existing_opp_ids = [row[0] for row in cursor.fetchall()]
    print(f"  Found {len(existing_opp_ids)} existing scores to migrate")
    
    # 2. Drop the old table
    cursor.execute("DROP TABLE IF EXISTS opportunity_score")
    
    # 3. Recreate with new schema
    cursor.execute("""
        CREATE TABLE opportunity_score (
            id VARCHAR(36) NOT NULL PRIMARY KEY,
            opportunity_id VARCHAR(36) NOT NULL UNIQUE,
            user_pain FLOAT,
            business_impact FLOAT,
            reach FLOAT,
            evidence_strength FLOAT,
            composite_score FLOAT,
            dimension_weights JSON,
            scored_at DATETIME,
            FOREIGN KEY(opportunity_id) REFERENCES opportunity(id)
        )
    """)
    cursor.execute("CREATE INDEX idx_opp_score_composite ON opportunity_score (composite_score)")
    
    # 4. Insert placeholder rows for existing opportunities (will be re-scored by the rescore script)
    import uuid
    from datetime import datetime
    
    weights = '{"user_pain": 7, "business_impact": 6, "reach": 4, "evidence_strength": 3}'
    now = datetime.utcnow().isoformat()
    
    for opp_id in existing_opp_ids:
        # Default scores = 3.0 each → composite = 7*3 + 6*3 + 4*3 + 3*3 = 60
        cursor.execute(
            """INSERT INTO opportunity_score 
               (id, opportunity_id, user_pain, business_impact, reach, evidence_strength, composite_score, dimension_weights, scored_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (str(uuid.uuid4()), opp_id, 3.0, 3.0, 3.0, 3.0, 60.0, weights, now)
        )
    
    conn.commit()
    print(f"  ✅ Migration complete. {len(existing_opp_ids)} scores migrated with default values.")
    print("  Run rescore_opportunities.py to score with LLM.")
    conn.close()

if __name__ == "__main__":
    migrate()
