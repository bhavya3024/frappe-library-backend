import sys
from fastapi import APIRouter, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import services.frappeLibrary
from utils.index import ResponseExecption
sys.path.append("../services/frappeLibrary.py")

frappeLibrary = services.frappeLibrary

router = APIRouter()


class ImportBooksDto(BaseModel):
    frappeBookIsbnNumbers: List[int]


@router.get("/")
def get_frappe_books(page: int = 1, title: str = ""):
    frappe_books = frappeLibrary.get_books(page, title)
    frappe_books = frappeLibrary.check_frappe_book_is_imported(frappe_books)
    return JSONResponse({
        "success": True,
        "status_code": 200,
        "frappe_books": jsonable_encoder(frappe_books)
    })


    


@router.post('/import-books')
def import_books(body: ImportBooksDto):
   try:
      frappeLibrary.import_books(body.frappeBookIsbnNumbers)
      return JSONResponse({
          "success": True,
          "status_code": 201,
          "message": "Frappe book has been successfully imported"
      })
   except ResponseExecption as e:
        print(e)
        raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")     


@router.get('/import-books/all')
def import_all_books():
    Response("Import book process has been started", media_type="text/plain")
    return frappeLibrary.import_all_books()


