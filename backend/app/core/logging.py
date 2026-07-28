"""
EduGuide Logging Configuration

Configures the application logger using Python's built-in logging module.
Log level is driven by the LOG_LEVEL environment variable.

Design: Keeping logging simple and dependency-free at this stage.
Structured JSON logging (e.g. structlog) can be added in a later phase
if observability requirements demand it.
"""

import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    """Configure the root logger for the application.

    Should be called once during application startup (lifespan).
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Silence noisy third-party loggers in non-debug mode.
    if not settings.DEBUG:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        "Logging configured | level=%s | environment=%s",
        settings.LOG_LEVEL,
        settings.ENVIRONMENT,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for use in application modules.

    Usage:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
