import sys
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import services.book
sys.path.append("../services/book.py")

bookService = services.book

router = APIRouter()


class BookStockDto(BaseModel):
    stock_amount: int


class BookIdStockDto(BaseModel):
    id: int
    stock_amount: int


class BookIdStocksDto(BaseModel):
    bookStocks: List[BookIdStockDto]


@router.get("/")
def get_books(page: int = 1, limit: int = 10):
    books = bookService.get_all_books(page, limit)
    booksCount = bookService.get_books_count()
    return JSONResponse({
        "success": True,
        "books": jsonable_encoder(books),
        "booksCount": booksCount
    })


@router.get('/{id}')
def get_book_details(id: int):
    book = bookService.get_book_detail(id)
    return JSONResponse({
        "success": True,
        "book": jsonable_encoder(book)
    })


@router.patch('/{id}/stock-amounts')
def update_stocks(id: int, body: BookStockDto):
    book = bookService.update_book(id, body.stock_amount)
    return JSONResponse({
        "success": True if book["status"] is 200 else False,
        "message": book["message"],
        "status_code": book["status"]
    })


@router.get('/{id}/members')
def get_book_members(id=int, page=int, limit:int = 10, add_new_members:bool = False):
    if add_new_members is True:
       book_members = bookService.get_add_new_book_members(id, int(limit), int(page))
       members_count = bookService.get_new_book_members_count(id)
       return JSONResponse({
        "success": True,
        "newMembers": jsonable_encoder(book_members),
        "membersCount": members_count,
       })
    else:    
       book_members = bookService.get_book_members_by_book_id(id, int(limit), int(page))
       book_members_count = bookService.get_book_members_count(id)
       return JSONResponse({
        "success": True,
        "bookMembers": jsonable_encoder(book_members),
        "bookMembersCount": jsonable_encoder(book_members_count)
       })

@router.patch('/stock-amounts/bulk')
def update_bulk_stocks(body: BookIdStocksDto):
    bookService.update_all_books(body.bookStocks)
    return JSONResponse({
        "success": True,
        "message": "Book stock amounts has been updated successfully",
        "status_code": 204
    })


