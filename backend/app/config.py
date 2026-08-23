from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # CORS — accepts a comma-separated string from env or a list
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000"]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database — defaults to local SQLite; Railway sets DATABASE_URL to PostgreSQL
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/discovery_engine.db"
    CHROMADB_PATH: str = "./data/chroma"

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v
    
    # Groq API
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GROQ_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    GROQ_MAX_CONCURRENT: int = 10
    GROQ_TIMEOUT: int = 30
    
    # Pipeline Settings
    PIPELINE_BATCH_SIZE: int = 50
    PIPELINE_MIN_CLUSTER_SIZE: int = 3
    PIPELINE_MIN_PATTERN_OCCURRENCES: int = 3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
