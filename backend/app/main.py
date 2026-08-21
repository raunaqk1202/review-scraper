# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="Discovery Intelligence Engine API",
    version="1.0.0",
    description="Backend API for the AI-Powered Fashion Purchase Discovery Engine",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.router import api_router

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.APP_ENV}

app.include_router(api_router, prefix="/api/v1")
