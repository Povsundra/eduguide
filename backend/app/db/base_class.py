import re

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

# Naming convention for constraints to ensure Alembic autogenerates names correctly
# and prevents migration errors across different databases.
POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


def camel_to_snake(name: str) -> str:
    """Convert CamelCase class names to snake_case table names."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy 2.0 declarative models.
    """

    metadata = metadata

    # Automatically generate __tablename__ based on class name
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
