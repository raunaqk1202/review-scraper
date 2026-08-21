import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient
from app.db.session import Base
from app.main import app

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    from app.models.feedback import DataSource, FeedbackItem
    from app.models.signals import AISignal
    from app.models.clusters import Cluster, ClusterMembership
    from app.models.patterns import Pattern, PatternEvidence
    from app.models.opportunities import Opportunity, OpportunityScore, OpportunityEvidence
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture to provide a database session for a test."""
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
def client() -> TestClient:
    """Fixture to provide a test client for the FastAPI app."""
    # To mock the DB dependency in routes, we'd override it here:
    # app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
    return TestClient(app)
