"""create votes table

Revision ID: 873937098193
Revises: acf85cefa422
Create Date: 2024-10-21 15:27:20.166089

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "873937098193"
down_revision: Union[str, None] = "acf85cefa422"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("poll_id", sa.Integer(), nullable=False),
        sa.Column("choice_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["choice_id"],
            ["options.id"],
        ),
        sa.ForeignKeyConstraint(
            ["poll_id"],
            ["polls.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("votes")
