import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

@pytest.mark.asyncio
async def test_rollback_isolation_insert(db_session: AsyncSession):
    """
    First test inserts data into the database and commits it.
    """
    user = User(email="test_rollback@example.com", is_active=True)
    db_session.add(user)
    await db_session.commit()
    
    result = await db_session.execute(text("SELECT COUNT(*) FROM user"))
    assert result.scalar() == 1

@pytest.mark.asyncio
async def test_rollback_isolation_verify(db_session: AsyncSession):
    """
    Second test verifies that the database is completely clean,
    proving that the table teardown/rollback strategy works flawlessly.
    """
    result = await db_session.execute(text("SELECT COUNT(*) FROM user"))
    assert result.scalar() == 0
