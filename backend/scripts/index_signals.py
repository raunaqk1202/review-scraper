import asyncio
import os
import chromadb
from chromadb.config import Settings
from app.db.session import AsyncSessionLocal as async_session
from app.models.signals import AISignal
from sqlalchemy.future import select

# We initialize ChromaDB to store data locally in backend/data/chroma
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "chroma")
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

# Get or create the collection
collection = client.get_or_create_collection(
    name="behavioral_signals",
    metadata={"hnsw:space": "cosine"} # Use cosine similarity for text search
)

async def index_signals():
    async with async_session() as db:
        result = await db.execute(select(AISignal))
        signals = result.scalars().all()
        
        if not signals:
            print("No signals found in SQLite to index.")
            return

        print(f"Loaded {len(signals)} signals from SQLite.")
        
        documents = []
        metadatas = []
        ids = []
        
        for sig in signals:
            # The "document" is the text we actually want to embed and search against.
            # We embed both the summary of the behavior and the exact verbatim quote.
            doc_text = f"Journey Stage: {sig.journey_stage}\nBehavior Summary: {sig.summary}\nVerbatim Quote: {sig.evidence_quote}"
            
            documents.append(doc_text)
            
            # Metadata is useful for filtering results later (e.g. "Only search WISHLIST stage")
            metadatas.append({
                "journey_stage": sig.journey_stage or "UNKNOWN",
                "signal_type": sig.signal_type or "UNKNOWN",
                "confidence_score": sig.confidence_score or 0.0
            })
            
            ids.append(sig.id)
            
        print("Embedding and inserting into ChromaDB... (This may take a moment to download the embedding model on first run)")
        
        # Chroma handles batching and embedding automatically
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Successfully indexed {len(ids)} signals into ChromaDB at {CHROMA_DB_DIR}")

if __name__ == "__main__":
    asyncio.run(index_signals())
