"""
Health Check Endpoint

Scope (Sub-Phase 1.2): Stub response only.
Real connectivity checks for PostgreSQL, Neo4j, and Redis
are wired in Sub-Phase 1.5.
"""

from fastapi import APIRouter, Depends, HTTPException
from neo4j import AsyncSession as Neo4jAsyncSession
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.neo4j import get_neo4j_session
from app.db.session import get_db

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
    postgres: str
    neo4j: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the health status of the API and connected databases.",
)
async def health_check(
    db: AsyncSession = Depends(get_db),
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session),
) -> HealthResponse:
    """Verifies API health and database connectivity."""
    postgres_status = "ok"
    neo4j_status = "ok"

    try:
        # Check Postgres
        await db.execute(text("SELECT 1"))
    except Exception as e:
        postgres_status = f"error: {str(e)}"

    try:
        # Check Neo4j
        await neo4j_session.run("RETURN 1")
    except Exception as e:
        neo4j_status = f"error: {str(e)}"

    if postgres_status != "ok" or neo4j_status != "ok":
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "postgres": postgres_status,
                "neo4j": neo4j_status,
            },
        )

    return HealthResponse(status="ok", postgres=postgres_status, neo4j=neo4j_status)
