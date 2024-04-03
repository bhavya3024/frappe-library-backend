"""add-timestamps

Revision ID: 718f0cb9ed8b
Revises: a8bb40949a15
Create Date: 2024-03-30 18:54:28.609178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '718f0cb9ed8b'
down_revision: Union[str, None] = 'a8bb40949a15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()))
    op.add_column('books', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=func.now()))
    op.add_column('language_codes', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()))
    op.add_column('language_codes', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=func.now()))


def downgrade() -> None:
    op.drop_column('books', 'updated_at')
    op.drop_column('books', 'created_at')
    op.drop_column('language_codes', 'updated_at')
    op.drop_column('language_codes', 'created_at')
