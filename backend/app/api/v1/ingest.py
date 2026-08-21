from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.api.deps import get_db
from app.services.ingestion_service import ingestion_service
from app.models.feedback import DataSource, FeedbackItem

router = APIRouter()

class IngestRequest(BaseModel):
    platform: str
    limit: int = 50
    kwargs: Optional[Dict[str, Any]] = {}

class SourceResponse(BaseModel):
    id: str
    platform: str
    source_type: str
    description: str
    last_fetched: Optional[str] = None

@router.post("/", response_model=Dict[str, Any])
async def trigger_ingestion(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger data ingestion from a specified platform.
    """
    try:
        # Run synchronously here for simplicity, but could be pushed to background
        result = await ingestion_service.ingest_from_source(
            db=db,
            platform=request.platform,
            limit=request.limit,
            **(request.kwargs or {})
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sources", response_model=List[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    """
    List configured data sources.
    """
    result = await db.execute(select(DataSource))
    sources = result.scalars().all()
    
    return [
        SourceResponse(
            id=s.id,
            platform=s.platform,
            source_type=s.source_type,
            description=s.description or "",
            last_fetched=s.last_fetched.isoformat() if s.last_fetched else None
        )
        for s in sources
    ]

@router.get("/stats", response_model=Dict[str, Any])
async def ingest_stats(db: AsyncSession = Depends(get_db)):
    """
    Get statistics about ingested data.
    """
    # Total count
    total_result = await db.execute(select(func.count()).select_from(FeedbackItem))
    total_scraped = total_result.scalar() or 0
    
    # Get all platforms that have sources configured
    sources_result = await db.execute(select(DataSource.platform))
    all_platforms = [p for p in sources_result.scalars().all()]
    
    # Count by platform
    platform_result = await db.execute(
        select(FeedbackItem.source_platform, func.count(FeedbackItem.id))
        .group_by(FeedbackItem.source_platform)
    )
    db_platform_counts = dict(platform_result.all())
    
    # Merge them to ensure all sources show up, even with 0 counts
    platform_counts = {p: db_platform_counts.get(p, 0) for p in all_platforms}
    
    # Include any platform that has items but wasn't in DataSource (just in case)
    for p, count in db_platform_counts.items():
        if p not in platform_counts:
            platform_counts[p] = count
            
    return {
        "total_scraped": total_scraped,
        "platform_counts": platform_counts
    }
