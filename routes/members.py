import sys
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.membersDto import MembersDto
from utils.index import ResponseExecption
from typing import List
import services.members
sys.path.append("../services/members.py")

member_service = services.members

router = APIRouter()


@router.post("/")
def create_member(body: MembersDto):
    try:
        new_member_response = member_service.create_member(body)
        return JSONResponse({
            "status_code": 201,
            "message": "New member has been created",
            "data": jsonable_encoder(new_member_response)
        })
    except ResponseExecption as e:
        print(e)
        return JSONResponse({
            "status_code": e.status or 500,
            "message": e.message  or "Internal Server Error"
        })


@router.get("/")
def get_members(page: int = 1):
    try:
        new_member_response = member_service.get_members(page=page)
        members_count = member_service.get_members_count()
        return JSONResponse({
            "status_code": 200,
            "message": "Members has been fetched successfully",
            "data": jsonable_encoder(new_member_response),
            "count": members_count
        })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")  


@router.patch("/{id}")
def update_member(id: int, body: MembersDto):
    try:
        update_response = member_service.update_member(id=id,member=body)
        return JSONResponse({
            "status_code": 200,
            "message": "Member has been updated successfully",
            "data": jsonable_encoder(update_response)
        })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")  

@router.get('/{id}')
def get_member_by_id(id: int):
    try:
       member_response = member_service.get_member_by_id(id=id)
       pending_dues = member_service.get_member_pending_dues(id=id)
       return JSONResponse({
           "status_code": 200,
           "message": "Member has been fetched successfully",
           "pending_dues": jsonable_encoder(pending_dues),
           "data": jsonable_encoder(member_response)         
       })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")    

@router.delete('/{id}')
def delete_member(id: int):
    try:
       member_service.delete_member(id=id)
       return JSONResponse({
           "status_code": 200,
           "message": "Member has been deleted successfully",
       })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")  


@router.get('/{id}/books')
def get_books_by_member_id(id: int, page: int = 1):
    try:
       db_books = member_service.get_books_by_member_id(id=id, page=page)
       db_books_count = member_service.get_books_count(id=id)
       return JSONResponse({
           "status_code": 200,
           "data": db_books,
           "count": db_books_count,
           "message": "Member has been deleted successfully",
       })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")  
