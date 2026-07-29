"""empty

Revision ID: 0cad69d82435
Revises: d4a6d535e403
Create Date: 2026-07-29 14:26:01.377786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cad69d82435'
down_revision: Union[str, Sequence[str], None] = 'd4a6d535e403'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
