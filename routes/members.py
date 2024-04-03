import sys
from fastapi import APIRouter
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
        return JSONResponse({
            "status_code": 200,
            "message": "Members has been fetched successfully",
            "data": jsonable_encoder(new_member_response)
        })
    except ResponseExecption as e:
        print(e)
        return JSONResponse({
            "status_code": e.status or 500,
            "message": e.message  or "Internal Server Error"
        })


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
        return JSONResponse({
            "status_code": e.status or 500,
            "message": e.message  or "Internal Server Error"
        })

@router.get('/{id}')
def get_member_by_id(id: int):
    try:
       member_response = member_service.get_member_by_id(id=id)
       return JSONResponse({
           "status_code": 200,
           "message": "Member has been fetched successfully",
           "data": jsonable_encoder(member_response)         
       })
    except ResponseExecption as e:
        print(e)
        return JSONResponse({
            "status_code": e.status or 500,
            "message": e.message  or "Internal Server Error"
        })

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
        return JSONResponse({
            "status_code": e.status or 500,
            "message": e.message  or "Internal Server Error"
        })
    