from typing import List

from pydantic import BaseModel
from sqlalchemy import Integer

from models.books import BookModel
from sqlalchemy.orm import sessionmaker
from connections.db import engine

Session = sessionmaker(bind=engine)
from sqlalchemy.sql import select


def get_all_books(page: int = 1, limit: int = 10):
    session = Session()
    books = session.query(BookModel).limit(limit).offset((page - 1) * limit).all()
    session.close()
    return books


def get_books_count():
    session = Session()
    booksCount = session.query(BookModel).count()
    session.close()
    return booksCount

def get_book_detail(id:int):
    session = Session()
    book = session.query(BookModel).filter_by(id=id).first()
    session.close()
    return book



class BookIdStockDto(BaseModel):
    id: int
    stock_amount: int


def update_book(id: int, stock_amount: int):
    session = Session()
    book = session.query(BookModel).filter_by(id=id).first()
    if book is None:
        return {
            "message": "Book Not Found",
            "status": 404
        }
    else:
        book.stock_amount += stock_amount
        session.commit()
        session.close()
        return {
            "message": "Book's Stock Amount has been updated",
            "status": 200
        }


def update_all_books(book_stocks: List[BookIdStockDto]):
    book_ids = list(map(lambda book_stock: book_stock.id, book_stocks))
    session = Session()
    books = session.query(BookModel).filter(BookModel.id.in_(book_ids))
    for book in books:
        current_book_stock = next(filter(lambda book_stock: book_stock.id == book.id, book_stocks), None)
        if current_book_stock:
            book.stock_amount += current_book_stock.stock_amount
    session.commit()
    session.close()



