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
def get_books(page: int = 1):
    books = bookService.get_all_books(page)
    return JSONResponse({
        "success": True,
        "books": jsonable_encoder(books)
    })


@router.patch('/{id}/stock-amounts')
def update_stocks(id: int, body: BookIdStockDto):
    book = bookService.update_book(id, body.stock_amount)
    return JSONResponse({
        "success": True if book["status"] is 200 else False,
        "message": book["message"],
        "status_code": book["status"]
    })


@router.patch('/stock-amounts/bulk')
def update_bulk_stocks(body: BookIdStocksDto):
    bookService.update_all_books(body.bookStocks)
    return JSONResponse({
        "success": True,
        "message": "Book stock amounts has been updated successfully",
        "status_code": 204
    })


