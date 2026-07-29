import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a transactional scope around a series of operations.
    Useful for background tasks or scripts outside the FastAPI request lifecycle.
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


@asynccontextmanager
async def transaction_manager(session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """
    A context manager to run operations within a database transaction.
    Commits automatically on success, rolls back automatically on exception.
    """
    try:
        yield session
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Database transaction failed: {e}")
        raise
    except Exception as e:
        await session.rollback()
        logger.error(f"Unexpected error during transaction: {e}")
        raise


async def check_database_health(session: AsyncSession) -> bool:
    """
    Ping the database with a lightweight SELECT 1 to verify connectivity.
    """
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
