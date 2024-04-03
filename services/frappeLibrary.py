from psycopg2 import Date

from models.frappebookdto import FrappeBookDto
from models.books import BookModel
from models.languageCodes import LanguageCodeModel
import requests
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from connections.db import engine

Session = sessionmaker(bind=engine)

baseUrl = "https://frappe.io/api/method/frappe-library"


def get_books(page=1, title=""):
    response = requests.get(baseUrl, {
        "page": page,
        "title": title
    })
    if response.status_code == 200:
        return response.json()


def import_book(dto: FrappeBookDto):
    session = Session()
    authors_list = [author.strip() for author in dto.authors.split('/')]

    language_code = dto.language_code

    db_language_code = session.query(LanguageCodeModel).filter_by(language_code=language_code).first()

    if db_language_code is None:
        db_language_code = LanguageCodeModel(
            language_code=language_code
        )
        session.add(db_language_code)
        session.commit()

    language_code_id = db_language_code.id

    db_book = session.query(BookModel).filter_by(isbn=dto.isbn).first()
    month = 0
    date = 0
    year = 0

    if dto.publication_date != "0":
        publication_date_array = dto.publication_date.split('/')
        month = int(publication_date_array[0])
        date = int(publication_date_array[1])
        year = int(publication_date_array[2])

    if db_book:
        db_book.frappe_book_id = dto.bookID
        db_book.title = dto.title
        db_book.average_rating = dto.average_rating
        db_book.isbn = dto.isbn
        db_book.isbn13 = dto.isbn13
        db_book.num_pages = dto.num_pages
        db_book.ratings_count = dto.ratings_count
        db_book.language_code_id = language_code_id
        db_book.authors = authors_list
        db_book.publisher = dto.publisher
        db_book.publication_date = Date(year, month, date) if dto.publication_date != "0" else None
        db_book.stock_amount += dto.stock_amount
        session.commit()
    else:
        db_book = BookModel(
            frappe_book_id=dto.bookID,
            text_reviews_count=dto.text_reviews_count,
            title=dto.title,
            average_rating=dto.average_rating,
            isbn=dto.isbn,
            isbn13=dto.isbn13,
            num_pages=dto.num_pages,
            ratings_count=dto.ratings_count,
            language_code_id=language_code_id,
            authors=authors_list,
            publisher_name=dto.publisher,
            publication_date=Date(year, month, date) if dto.publication_date != "0" else None,
            stock_amount=dto.stock_amount
        )
        session.add(db_book)
        session.commit()
    return db_book


def import_books(isbn_numbers: List[Dict[str, str]]):
    for isbnNumber in isbn_numbers:
        response = requests.get(baseUrl, {
            "isbn": isbnNumber['isbn_number']
        })
        if response.status_code == 200:
            json = response.json()
            fdto = FrappeBookDto(json['message'][0])
            import_book(fdto, isbnNumber['stock'])


def import_all_books():
    page = 1
    while True:
        response = requests.get(baseUrl, {
            "page": page
        })
        print(page)
        if response.status_code == 200:
            json = response.json()
            if len(json['message']) == 0:
                break
            else:
                page += 1
                for book in json['message']:
                    try:
                        fdto = FrappeBookDto(book)
                        import_book(fdto)
                    except Exception as e:
                        print(e)
