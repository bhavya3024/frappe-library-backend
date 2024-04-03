"""add-stocks

Revision ID: a8bb40949a15
Revises: 77c2d1c5f6f7
Create Date: 2024-03-28 01:50:55.463837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a8bb40949a15'
down_revision: Union[str, None] = '77c2d1c5f6f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('stock_amount', sa.Integer(), server_default=0))



def downgrade() -> None:
   op.drop_column('books', 'stock_amount')