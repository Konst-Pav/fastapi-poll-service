"""create polls and options tables

Revision ID: acf85cefa422
Revises: 
Create Date: 2024-10-01 14:44:35.425960

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "acf85cefa422"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "polls",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "options",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("point", sa.String(), nullable=False),
        sa.Column("poll_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["poll_id"],
            ["polls.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("options")
    op.drop_table("polls")
