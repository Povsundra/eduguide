import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base_class import Base

# We use an in-memory SQLite database for testing perfectly isolated
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """
    Creates a global test engine for the session.
    Uses StaticPool to ensure the same in-memory database is shared across connections.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL, 
        echo=False,
        poolclass=StaticPool,
        connect_args={'check_same_thread': False}
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine):
    """
    Creates a new database session for a test.
    Automatically creates all tables before the test and drops them after,
    ensuring a perfectly clean state and rollback verification for every test.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_factory() as session:
        yield session
        
    # Drop tables after test completes to clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
