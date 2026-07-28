"""
API v1 Router

Single mount point for all v1 endpoints.
Future endpoints (recommend, compare, search, chat, etc.)
are registered here as they are implemented in later phases.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

router = APIRouter()

# Health check — available at /api/v1/health
router.include_router(health.router)
