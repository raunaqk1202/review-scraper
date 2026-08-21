from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

# Detect database type from the URL scheme
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Build engine kwargs conditionally
_engine_kwargs: dict = {
    "echo": (settings.APP_ENV == "development"),
}

if _is_sqlite:
    # SQLite requires check_same_thread=False for async / multi-thread use
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

# Create session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
