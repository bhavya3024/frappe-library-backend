from psycopg2 import Date

from models.bookMemberDto import BookMembersDto
from models.members import MembersModel
from models.bookMembers import BookMembersModel
from models.books import BookModel
from typing import List, Dict
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import and_, func
from connections.db import engine
from fastapi.encoders import jsonable_encoder
from utils.index import ResponseExecption

SessionMaker = sessionmaker(bind=engine)

def check_dues(member_id:int, session: Session):
    dues = session.query(func.sum(BookMembersModel.price)).filter(BookMembersModel.rent_paid == False, BookMembersModel.member_id == member_id).scalar()
    if dues > 500:
        raise ResponseExecption(status=403, message="You have to pay outstanding dues first")

def create_book_member(book_member: BookMembersDto):
    session = SessionMaker()
    db_member = session.query(MembersModel).filter_by(id=book_member.member_id).first()
    db_book = session.query(BookModel).filter_by(id=book_member.book_id).first()
    if db_member is None:
        session.close()
        raise ResponseExecption(status=404, message='Member not found')
    if db_book is None:
        session.close()
        raise ResponseExecption(status=404, message='Member with this email already exists')
    if db_book.stock_amount < 1:
        session.close()
        raise ResponseExecption(status=400, message='This book is out of stock for now')
    difference = book_member.rent_end_date - book_member.rent_start_date
    if difference.days < 1:
        raise ResponseExecption(status=400, message="You need to rent a book for atleast one day")
    if difference.days > 30:
        raise ResponseExecption(status=400, message="You can maximum rent a box for 30 days")
    price = difference.days * 25 # taken simple formula for simplicity
    db_book_member = BookMembersModel(
        book_id=book_member.book_id,
        member_id=book_member.member_id,
        price=price,
        rent_start_date=book_member.rent_start_date,
        rent_end_date=book_member.rent_end_date,
    )
    db_book.stock_amount -= 1
    session.commit()
    session.close()
    return db_book_member


def get_book_member(page=1):
    session = SessionMaker()
    members = session.query(MembersModel).filter().limit(10).offset((page -1) * 10).all()
    return members


def update_member(member=MembersDto, id=int):
    session = SessionMaker()
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
    session = SessionMaker()
    db_member = session.query(MembersModel).filter_by(id=id).first()
    session.close()
    if db_member is None:
        raise ResponseExecption(status=404, message="Member not Found")
    return db_member


def delete_member(id=int):
    session = SessionMaker()
    session.query(MembersModel).delete(id=id)
    session.commit()

