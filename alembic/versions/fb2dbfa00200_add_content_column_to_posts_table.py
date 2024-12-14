"""add content column to posts table

Revision ID: fb2dbfa00200
Revises: 0337bb22485d
Create Date: 2024-12-14 17:36:24.271706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb2dbfa00200'
down_revision: Union[str, None] = '0337bb22485d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    

def downgrade():
    op.drop_column('posts', 'content')
