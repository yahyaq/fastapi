"""add content column to posts table

Revision ID: 05697751355d
Revises: 65868959b4ec
Create Date: 2024-10-07 13:42:29.550648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05697751355d'
down_revision: Union[str, None] = '65868959b4ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
