from sqlalchemy import ARRAY, DateTime, func

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    frappe_book_id = Column(Integer, name='frappe_book_id')
    title = Column(String)
    average_rating = Column(Float, name='average_rating')  # Assuming average_rating is a float
    isbn = Column(String, unique=True, name='isbn')
    isbn13 = Column(String, unique=True, name='isbn13')
    num_pages = Column(Integer, name='num_pages')  # Assuming num_pages is an integer
    ratings_count = Column(Integer, name='ratings_count')  # Assuming ratings_count is an integer
    text_reviews_count = Column(Integer, name='text_reviews_count')  # Assuming text_reviews_count is an integer
    publication_date = Column(Date, name='publication_date')  # Assuming publication_date is a date
    authors = Column(ARRAY(String), name='authors')
    publisher_name = Column(String, name='publisher_name')
    language_code_id = Column(Integer, name='language_code_id')
    stock_amount = Column(Integer, name='stock_amount')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
