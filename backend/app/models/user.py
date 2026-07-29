from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class User(Base, UUIDMixin, TimestampMixin):
    """
    Dummy user model to initialize Alembic migrations.
    Will be expanded in the Authentication phase.
    """

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
