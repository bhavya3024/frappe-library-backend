from sqlalchemy import ARRAY, DateTime, func

from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# def upgrade() -> None:
#     op.create_table(
#         'book_members',
#         sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
#         sa.Column('book_id', sa.Integer(), nullable=False),
#         sa.Column('member_id', sa.Integer(), nullable=True),
#         sa.Column('rent_start_date', sa.DateTime(), nullable=False),
#         sa.Column('rent_end_date', sa.DateTime(), nullable=False),
#         sa.Column('price', sa.Float(), nullable=False), # price will be no of days book has been kept
#         sa.Column('rent_paid', sa.Boolean(), nullable=False, server_default=sa.false()),
#         sa.Column('rent_paid_at', sa.DateTime(), nullable=False),
#         sa.Column('created_at', sa.DateTime(), nullable=False,server_default=sa.func.now()),
#         sa.Column('updated_at', sa.DateTime(), nullable=False,server_default=sa.func.now(), onupdate=sa.func.now()),        
#         sa.PrimaryKeyConstraint('id'),
#         sa.UniqueConstraint('book_id', 'member_id'),

class BookMembersModel(Base):
    __tablename__ = 'book_members'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer,nullable=False),
    member_id = Column(Integer,nullable=False),
    rent_start_date=Column(DateTime, nullable=False),
    rent_end_date=Column(DateTime, nullable=False),
    rent_paid=Column(Boolean, nullable=False),
    rent_paid_at=Column(DateTime, nullable=False),
    price=Column(Integer,nullable=False),
    created_at = Column(DateTime, name='created_at', default=func.now())
    updated_at = Column(DateTime, name='updated_at', default=func.now(), onupdate=func.now())
