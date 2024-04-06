from sqlalchemy import ARRAY, DateTime, func

from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class BookMembersModel(Base):
    __tablename__ = 'book_members'
    id = Column(Integer, primary_key=True, name='id')
    book_id = Column(Integer,nullable=False, name='book_id')
    member_id = Column(Integer,nullable=False, name='member_id')
    rent_start_date = Column(DateTime, nullable=False, name='rent_start_date')
    rent_end_date = Column(DateTime, nullable=False, name='rent_end_date')
    rent_paid = Column(Boolean, nullable=False, name='rent_paid')
    rent_paid_at = Column(DateTime, nullable=True, name='rent_paid_at')
    price = Column(Integer,nullable=False, name='price')
    created_at = Column(DateTime, name='created_at', default=func.now())
    updated_at = Column(DateTime, name='updated_at', default=func.now(), onupdate=func.now())
