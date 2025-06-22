"""add bookings

Revision ID: dfdf00e220c4
Revises: 9d2baea20bcf
Create Date: 2025-02-10 01:07:01.950665

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dfdf00e220c4"
down_revision: Union[str, None] = "9d2baea20bcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.DateTime(), nullable=False),
        sa.Column("date_to", sa.DateTime(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
