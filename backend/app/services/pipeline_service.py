from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.pipeline.orchestrator import PipelineOrchestrator
from app.pipeline.stage_1_cleaning import Stage1Cleaning
from app.pipeline.stage_2_enrichment import Stage2Enrichment
from app.pipeline.stage_3_clustering import Stage3Clustering
from app.pipeline.stage_4_patterns import Stage4Patterns
from app.pipeline.stage_5_opportunities import Stage5Opportunities

class PipelineService:
    def __init__(self):
        self.orchestrator = PipelineOrchestrator()
        self.orchestrator.register_stage(Stage1Cleaning())
        self.orchestrator.register_stage(Stage2Enrichment())
        self.orchestrator.register_stage(Stage3Clustering())
        self.orchestrator.register_stage(Stage4Patterns())
        self.orchestrator.register_stage(Stage5Opportunities())
        
        self.runs = {}

    async def run_pipeline(self, db: AsyncSession, stages: List[int] = None) -> Dict[str, Any]:
        result = await self.orchestrator.run(db, stages)
        self.runs[result["run_id"]] = result
        return result
        
    def get_status(self) -> Dict[str, Any]:
        return self.runs

pipeline_service = PipelineService()
