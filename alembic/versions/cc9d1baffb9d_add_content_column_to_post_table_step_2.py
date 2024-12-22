"""add content column to post table
step 2

Revision ID: cc9d1baffb9d
Revises: 24762a2dec60
Create Date: 2024-12-21 18:39:49.497735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc9d1baffb9d'
down_revision: Union[str, None] = '24762a2dec60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass