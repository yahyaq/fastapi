"""add the remaining columns to posts table

Revision ID: bc7755541cb3
Revises: 635fcc71e253
Create Date: 2024-10-07 16:18:59.062229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc7755541cb3'
down_revision: Union[str, None] = '635fcc71e253'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('publish', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'publish')
    op.drop_column('posts', 'created_at')
    pass
