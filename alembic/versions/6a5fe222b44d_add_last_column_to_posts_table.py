"""add last column to posts table

Revision ID: 6a5fe222b44d
Revises: 1361a023eab8
Create Date: 2024-12-14 17:53:26.679640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5fe222b44d'
down_revision: Union[str, None] = '1361a023eab8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')