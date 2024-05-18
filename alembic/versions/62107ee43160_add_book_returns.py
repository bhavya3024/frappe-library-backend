"""add-book-returns

Revision ID: 62107ee43160
Revises: bde4cca0aed5
Create Date: 2024-05-18 22:50:17.978997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62107ee43160'
down_revision: Union[str, None] = 'bde4cca0aed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book_members', sa.Column('is_returned', sa.BOOLEAN(), server_default=sa.text('False')))



def downgrade() -> None:
   op.drop_column('book_members', 'book_returned')
