from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1160479c1488'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('frappe_book_id', sa.Integer(), nullable=False, unique=True, autoincrement=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('average_rating', sa.Float(), nullable=True),
        sa.Column('isbn', sa.String(), nullable=False),
        sa.Column('isbn13', sa.String(), nullable=False),
        sa.Column('num_pages', sa.Integer(), nullable=False),
        sa.Column('ratings_count', sa.Integer(), nullable=False),
        sa.Column('text_reviews_count', sa.Integer(), nullable=False),
        sa.Column('publication_date', sa.Date(), nullable=True),
        sa.Column('authors', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('publisher_name', sa.String(), nullable=False),
        sa.Column('language_code_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade() -> None:
    op.drop_table('books')
