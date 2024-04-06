import sys
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.bookMemberDto import BookMembersDto
from typing import List
from utils.index import  ResponseExecption
import services.bookMembers
sys.path.append("../services/bookMembers.py")

bookService = services.bookMembers

router = APIRouter()


@router.post("/")
def add_book_member(body: BookMembersDto):
  try:
    book_member_response = bookService.create_book_member(body)
    return JSONResponse({
        "success": True,
        "book_members": jsonable_encoder(book_member_response)
    })
  except ResponseExecption as e:
    print(e)
    return JSONResponse({
        "status_code": e.status or 500,
        "message": e.message  or "Internal Server Error"
    })

@router.get("/")
def get_book_members(page=1, member_id:int = None):
    try:
      book_members = bookService.get_book_members(page, member_id)
      return JSONResponse({
        "success": True,
        "book_members": jsonable_encoder(book_members),
      })
    except ResponseExecption as e:
      print(e)
      return JSONResponse({
        "status_code": e.status or 500,
        "message": e.message  or "Internal Server Error"
      })


@router.patch('/{id}/pay-dues')
def pay_dues(id=1):
   try:
     bookService.pay_dues(id=id)
     return JSONResponse({
         "success": True,
         "message": "Rent has been paid successfully"
     })
   except ResponseExecption as e:
     print(e)
     return JSONResponse({
       "status_code": e.status or 500,
       "message": e.message or "Internal Server Error"
     })

   

