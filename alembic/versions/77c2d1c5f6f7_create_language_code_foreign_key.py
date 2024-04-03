"""create-language-code-foreign-key

Revision ID: 77c2d1c5f6f7
Revises: c4bc695ff6b0
Create Date: 2024-03-24 22:30:11.505359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '77c2d1c5f6f7'
down_revision: Union[str, None] = 'c4bc695ff6b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fk_books_language_id', 'books', 'language_codes', ['language_code_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_books_language_id', 'books', type_='foreignkey')

    # ### end Alembic commands ###
