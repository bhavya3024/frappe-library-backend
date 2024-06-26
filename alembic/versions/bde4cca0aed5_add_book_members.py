"""add-book-members

Revision ID: bde4cca0aed5
Revises: 086db3d03c5b
Create Date: 2024-03-31 00:51:58.533632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bde4cca0aed5'
down_revision: Union[str, None] = '086db3d03c5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'book_members',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=True),
        sa.Column('rent_start_date', sa.DateTime(), nullable=False),
        sa.Column('rent_end_date', sa.DateTime(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False), # price will be no of days book has been kept
        sa.Column('rent_paid', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('rent_paid_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False,server_default=sa.func.now(), onupdate=sa.func.now()),        
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key('fk_books_id', 'book_members', 'books', ['book_id'], ['id'])
    op.create_foreign_key('fk_member_id', 'book_members', 'members', ['member_id'], ['id'])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_books_id', 'book_members', type_='foreignkey')
    op.drop_constraint('fk_member_id', 'book_members', type_='foreignkey')
    op.drop_table('book_members')
