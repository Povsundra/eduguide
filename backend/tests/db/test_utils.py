import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.utils import check_database_health, transaction_manager



@pytest.mark.asyncio
async def test_check_database_health(db_session: AsyncSession):
    is_healthy = await check_database_health(db_session)
    assert is_healthy is True

@pytest.mark.asyncio
async def test_transaction_manager_commit(db_session: AsyncSession):
    # Setup dummy table
    await db_session.execute(text("CREATE TABLE test_tx (id INTEGER PRIMARY KEY, val TEXT)"))
    await db_session.commit()
    
    async with transaction_manager(db_session):
        await db_session.execute(text("INSERT INTO test_tx (val) VALUES ('success')"))
        
    # Transaction manager should auto-commit
    result = await db_session.execute(text("SELECT val FROM test_tx WHERE id = 1"))
    assert result.scalar() == "success"

@pytest.mark.asyncio
async def test_transaction_manager_rollback(db_session: AsyncSession):
    # Setup dummy table
    await db_session.execute(text("CREATE TABLE test_rb (id INTEGER PRIMARY KEY, val TEXT)"))
    await db_session.commit()
    
    with pytest.raises(Exception):
        async with transaction_manager(db_session):
            await db_session.execute(text("INSERT INTO test_rb (val) VALUES ('failed')"))
            raise ValueError("Triggering rollback")
            
    # Transaction manager should auto-rollback
    result = await db_session.execute(text("SELECT COUNT(*) FROM test_rb"))
    assert result.scalar() == 0

@pytest.mark.asyncio
async def test_get_session_context(monkeypatch):
    # We patch AsyncSessionLocal so it yields a mocked async session using our test engine
    from app.db.utils import get_session_context
    import app.db.utils
    
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    mock_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    monkeypatch.setattr(app.db.utils, "AsyncSessionLocal", mock_sessionmaker)
    
    async with get_session_context() as session:
        assert isinstance(session, AsyncSession)
        assert session.is_active is True
        # just do a query to prove it works
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
        
    # the session should be closed now
