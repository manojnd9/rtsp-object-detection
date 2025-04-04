"""add stream name

Revision ID: 16a45a7d0f57
Revises: 778ece3f04f8
Create Date: 2025-03-24 00:01:28.252268

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "16a45a7d0f57"
down_revision: Union[str, None] = "778ece3f04f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "stream_sessions", sa.Column("stream_name", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("stream_sessions", "stream_name")
    # ### end Alembic commands ###
