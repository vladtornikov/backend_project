"""users add unique email

Revision ID: 9d2baea20bcf
Revises: d0ad593eb769
Create Date: 2025-01-29 02:55:26.026421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "9d2baea20bcf"
down_revision: Union[str, None] = "d0ad593eb769"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
