from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.services.pipeline_service import pipeline_service

router = APIRouter()

class PipelineRunRequest(BaseModel):
    stages: Optional[List[int]] = None

@router.post("/run", response_model=Dict[str, Any])
async def trigger_pipeline(
    request: PipelineRunRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger the AI pipeline stages.
    """
    try:
        # For MVP we run this synchronously, but normally push to background
        result = await pipeline_service.run_pipeline(db, request.stages)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=Dict[str, Any])
async def get_pipeline_status():
    """
    Get the status of pipeline runs.
    """
    return pipeline_service.get_status()
