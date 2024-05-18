import sys
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.bookMemberDto import BookMembersDto
from typing import List
from utils.index import  ResponseExecption
import services.bookMembers
sys.path.append("../services/bookMembers.py")

bookMemberService = services.bookMembers

router = APIRouter()


@router.post("/")
def add_book_member(body: BookMembersDto):
  try:
    book_member_response = bookMemberService.create_book_member(body)
    return JSONResponse({
        "success": True,
        "book_members": jsonable_encoder(book_member_response)
    })
  except ResponseExecption as e:
      print(e)
      raise HTTPException(400, e.message or "Internal Server Error")  

@router.get("/")
def get_book_members(page=1, member_id:int = None):
    try:
      book_members = bookMemberService.get_book_members(member_id=member_id, page=int(page))
      return JSONResponse({
        "success": True,
        "book_members": jsonable_encoder(book_members),
      })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")


@router.patch('/{id}/pay-dues')
def pay_dues(id=1):
   try:
     bookMemberService.pay_dues(id=id)
     return JSONResponse({
         "success": True,
         "message": "Rent has been paid successfully"
     })
   except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")

   
@router.get('/{id}/returns')
def return_book(id=1):
   try:
      bookMemberService.return_book(id=id)
      return JSONResponse({
         "success": True,
         "message": "Book has been returned successfully"
      })
   except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")
   