from psycopg2 import Date

from models.membersDto import MembersDto
from models.members import MembersModel
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from connections.db import engine
from fastapi.encoders import jsonable_encoder
from utils.index import ResponseExecption

Session = sessionmaker(bind=engine)

baseUrl = "https://frappe.io/api/method/frappe-library"



def create_member(member=MembersDto):
    session = Session()
    db_member = session.query(MembersModel).filter_by(email=member.email).first()
    if db_member:
        session.close()
        raise ResponseExecption(status=409, message='Member with this email already exists')
    else:
        db_member = MembersModel(
            first_name=member.first_name,
            middle_name=member.middle_name,
            last_name=member.last_name,
            email=member.email,
        )
        session.add(db_member)
        session.commit()
        session.close()
    return db_member


def get_members(page=1):
    session = Session()
    members = session.query(MembersModel).filter().limit(10).offset((page -1) * 10).all()
    return members


def update_member(member=MembersDto, id=int):
    session = Session()
    db_member = session.query(MembersModel).filter_by(id=id).first()
    if db_member is None:
        raise ResponseExecption(status=404, message="Member not Found")
    if member.first_name:
        db_member.first_name = member.first_name
    if member.middle_name:
        db_member.middle_name = member.middle_name
    if member.last_name:
        db_member.last_name = member.last_name
    if member.email:
        another_member_with_same_email = session.query(MembersModel).filter(and_(MembersModel.id != db_member.id, MembersModel.email == member.email)).first()
        if another_member_with_same_email:
            session.close()
            raise ResponseExecption(status=404, message="Another member having same email exists")
        else: 
            db_member.email = member.email
    session.commit()
    session.close()


def get_member_by_id(id=int):
    session = Session()
    db_member = session.query(MembersModel).filter_by(id=id).first()
    session.close()
    if db_member is None:
        raise ResponseExecption(status=404, message="Member not Found")
    return db_member


def delete_member(id=int):
    session = Session()
    session.query(MembersModel).delete(id=id)
    session.commit()

