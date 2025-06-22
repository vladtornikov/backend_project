"""empty message

Revision ID: d0ad593eb769
Revises: bb48fe99f7f2
Create Date: 2025-01-29 01:40:20.636126

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d0ad593eb769"
down_revision: Union[str, None] = "bb48fe99f7f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=200), nullable=False)
    )
    op.drop_column("users", "password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "hashed_password")
