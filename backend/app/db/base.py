"""
Import all the models, so that Base has them before being imported by Alembic.
This allows Alembic to discover all the tables via Base.metadata.
"""

from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
