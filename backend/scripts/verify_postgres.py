import asyncio
import sys
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from app.db.session import engine, AsyncSessionLocal
from app.db.utils import check_database_health

async def main():
    logger.info("Verifying PostgreSQL Engine Configuration...")
    
    # 1. Verify pool settings
    pool = engine.pool
    logger.info(f"Pool size: {pool.size()}")
    logger.info(f"Max overflow: {pool._max_overflow}")
    logger.info(f"Pool pre_ping (health validation): {pool._pre_ping}")
    logger.info(f"Pool recycle (connection retry/refresh): {pool._recycle} seconds")
    logger.info(f"Pool timeout: {pool._timeout} seconds")
    
    # 2. Verify Database connection succeeds using health utility
    logger.info("Executing database health check...")
    async with AsyncSessionLocal() as session:
        is_healthy = await check_database_health(session)
        
    if is_healthy:
        logger.info("Database connection succeeds! Health check passed.")
    else:
        logger.error("Database connection failed!")
        sys.exit(1)
        
    logger.info("PostgreSQL validation completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
