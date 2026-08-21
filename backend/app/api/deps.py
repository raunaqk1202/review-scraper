import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import chromadb

from app.db.session import AsyncSessionLocal

# SQLite DB Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# ChromaDB Dependency
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "chroma")
_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return _chroma_client
