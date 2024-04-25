import json
from utils.index import convert_datetime_to_string, convert_query_result_to_json
from typing import List
from pydantic import BaseModel
from sqlalchemy import text
from models.books import BookModel
from models.bookMembers import BookMembersModel
from models.members import MembersModel
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


def get_book_members_count(id=int):
    session = Session()
    book_members_count = session.query(BookMembersModel).filter_by(book_id=id).count()
    session.close()
    return book_members_count


def matching_member(member):
    return member.id


def get_book_members_by_book_id( book_id: int, limit: int, page: int = 1):
    # Calculate the offset based on page number and limit

    session = Session()
    offset = (page - 1) * limit
    
    # Use a parameterized query to avoid SQL injection
    query = text('''
        SELECT book_members.*, members.first_name, members.last_name, members.email
        FROM book_members 
        INNER JOIN members ON book_members.member_id = members.id AND book_members.book_id = :book_id 
        LIMIT :limit 
        OFFSET :offset
    ''')

    # Execute the query with parameters
    results = session.execute(query, {'book_id': int(book_id), 'limit': int(limit), 'offset': int(offset)})
    rows = results.fetchall()
    json_data = convert_query_result_to_json(results, rows)
    return json_data



def get_add_new_book_members(book_id: int, limit: int, page: int = 1):
    session = Session()
    offset = (page - 1) * limit

    query = text('''
        select * from members m where id not in (
        select member_id from book_members bm where rent_paid = false group by member_id having sum(bm.price) > 500
        ) and id not in (
        select member_id from book_members bm where rent_paid = false and book_id = :book_id)
       LIMIT :limit OFFSET :offset
        '''
       )
    results = session.execute(query, {'book_id': int(book_id), 'limit': int(limit), 'offset': int(offset)})
    rows = results.fetchall()
    json_data = convert_query_result_to_json(results, rows)
    return json_data


def get_new_book_members_count(book_id=int):
    session = Session()

    query = text('''
        select count(*) from members m where id not in (
        select member_id from book_members bm where rent_paid = false group by member_id having sum(bm.price) > 500
        ) and id not in (
        select member_id from book_members bm where rent_paid = false and book_id = :book_id)
        '''
       )
    results = session.execute(query, {'book_id': int(book_id) })
    rows = results.fetchall()
    return rows[0][0]
