import uuid
import logging
from typing import List, Dict, Any, Type
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.pipeline.base import PipelineStage

logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    def __init__(self):
        self.stages: Dict[int, PipelineStage] = {}
        
    def register_stage(self, stage: PipelineStage):
        self.stages[stage.stage_number] = stage
        
    async def run(self, db: AsyncSession, stages_to_run: List[int] = None) -> Dict[str, Any]:
        run_id = str(uuid.uuid4())
        logger.info(f"Starting pipeline run {run_id}")
        
        results = {
            "run_id": run_id,
            "start_time": datetime.utcnow().isoformat(),
            "stages": {}
        }
        
        sorted_stages = sorted(self.stages.values(), key=lambda s: s.stage_number)
        if stages_to_run:
            sorted_stages = [s for s in sorted_stages if s.stage_number in stages_to_run]
            
        for stage in sorted_stages:
            logger.info(f"Running stage {stage.stage_number}: {stage.stage_name}")
            stage_result = {
                "name": stage.stage_name,
                "start_time": datetime.utcnow().isoformat(),
                "status": "RUNNING"
            }
            
            try:
                metrics = await stage.process(db)
                stage_result["metrics"] = metrics
                stage_result["status"] = "COMPLETED"
                stage_result["end_time"] = datetime.utcnow().isoformat()
            except Exception as e:
                logger.error(f"Error in stage {stage.stage_number}: {e}", exc_info=True)
                stage_result["status"] = "FAILED"
                stage_result["error"] = str(e)
                stage_result["end_time"] = datetime.utcnow().isoformat()
                results["stages"][stage.stage_number] = stage_result
                break # Stop pipeline on failure
                
            results["stages"][stage.stage_number] = stage_result
            
        results["end_time"] = datetime.utcnow().isoformat()
        results["status"] = "COMPLETED" if all(s["status"] == "COMPLETED" for s in results["stages"].values()) else "FAILED"
        return results

orchestrator = PipelineOrchestrator()
