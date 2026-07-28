"""
EduGuide API — Application Entry Point

Creates and configures the FastAPI application.

Architecture:
    - Lifespan context manager handles startup/shutdown hooks.
      Sub-Phase 1.5 will add DB connection pool management here.
    - CORS is configured from environment variables (never hardcoded).
    - All business routes are versioned under /api/v1/.
    - GET / is a root-level service metadata endpoint (not versioned).
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Lifespan — startup and shutdown hooks
# -----------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown events."""
    # --- Startup ---
    configure_logging()
    logger.info(
        "Starting %s v%s | environment=%s",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )

    # Initialize Neo4j driver
    from app.db.neo4j import close_neo4j, init_neo4j

    await init_neo4j()

    yield  # Application is running

    # --- Shutdown ---
    logger.info("Shutting down %s", settings.APP_NAME)
    await close_neo4j()


# -----------------------------------------------------------------------------
# Application factory
# -----------------------------------------------------------------------------


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "EduGuide — AI-powered educational guidance platform for Cambodia. "
            "Helps students discover universities, programs, scholarships, and careers."
        ),
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # -------------------------------------------------------------------------
    # CORS Middleware
    # Origins are controlled entirely by environment variable CORS_ORIGINS.
    # -------------------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------------------------------------------------------
    # Routes
    # -------------------------------------------------------------------------

    # Root — service metadata (not versioned)
    @app.get("/", tags=["root"], summary="Service Info")
    async def root() -> dict[str, str]:
        """Return basic service identification metadata."""
        return {
            "service": settings.APP_NAME,
            "status": "running",
            "version": settings.APP_VERSION,
        }

    # Root-level health — for Docker health checks and load balancers.
    # The versioned /api/v1/health (with real DB checks) is wired in Sub-Phase 1.5.
    @app.get("/health", tags=["health"], summary="Health Check")
    async def health() -> dict[str, str]:
        """Stub health check at root level.

        Returns:
            dict: Always returns status 'ok' in this phase.
        """
        return {"status": "ok"}

    # API v1 — all business endpoints
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

    return app


# -----------------------------------------------------------------------------
# Application instance
# Uvicorn entry point: uvicorn app.main:app
# -----------------------------------------------------------------------------

app = create_app()
