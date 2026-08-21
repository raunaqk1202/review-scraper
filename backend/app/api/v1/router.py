# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.api.v1 import opportunities, research, pipeline, ingest, evidence, segments, trends

api_router = APIRouter()
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
api_router.include_router(research.router, prefix="/research", tags=["research"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
api_router.include_router(segments.router, prefix="/segments", tags=["segments"])
api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
