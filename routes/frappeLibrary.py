import sys
from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import List, Dict
import services.frappeLibrary
sys.path.append("../services/frappeLibrary.py")

frappeLibrary = services.frappeLibrary

router = APIRouter()


class ImportBooksDto(BaseModel):
    frappeBookIds: List[Dict[str, str]]


@router.get("/")
def get_frappe_books(page: int = 1, title: str = ""):
    return frappeLibrary.get_books(page, title)


@router.post('/import-books')
def import_books(body: ImportBooksDto):
    return frappeLibrary.import_books(body.frappeBookIds)


@router.get('/import-books/all')
def import_all_books():
    Response("Import book process has been started", media_type="text/plain")
    return frappeLibrary.import_all_books()


