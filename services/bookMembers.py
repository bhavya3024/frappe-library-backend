from psycopg2 import Date

from models.bookMemberDto import BookMembersDto
from models.members import MembersModel
from models.bookMembers import BookMembersModel
from models.books import BookModel
from typing import List, Dict
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text, and_
from connections.db import engine
from utils.index import ResponseExecption
from datetime import datetime


SessionMaker = sessionmaker(bind=engine)

def check_dues(member_id:int, session: Session):
    query = text(f'SELECT SUM(price) from book_members WHERE member_id = {member_id}')
    dues = session.execute(query).scalar()
    print(f'Dues are --->>> ${dues}')
    if dues is None:
        return
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
    check_dues(book_member.member_id, session=session)
    difference = book_member.rent_end_date - book_member.rent_start_date
    if difference.days < 1:
        raise ResponseExecption(status=400, message="You need to rent a book for atleast one day")
    if difference.days > 30:
        raise ResponseExecption(status=400, message="You can maximum rent a box for 30 days")
    price = difference.days * 25 # taken simple formula for simplicity
    book_member_exists = session.query(BookMembersModel).filter_by(book_id=book_member.book_id, member_id=book_member.member_id).first()
    if book_member_exists and book_member_exists.rent_paid is False:
        raise ResponseExecption(status=400, message="Member has to pay rent for the same book took before")
    db_book_member = BookMembersModel(
        book_id=book_member.book_id,
        member_id=book_member.member_id,
        price=price,
        rent_start_date=book_member.rent_start_date,
        rent_end_date=book_member.rent_end_date,
        rent_paid=False
    )
    db_book.stock_amount -= 1
    session.add(db_book_member)
    session.commit()
    session.close()
    return db_book_member


def get_book_members(page=1, member_id=None):
    session = SessionMaker()
    book_member = session.query(BookMembersModel) 
    if member_id:
        book_member = book_member.filter(and_(BookMembersModel.member_id==member_id))
    book_member = book_member.limit(10).offset((page - 1) * 10).all()
    return book_member

def pay_dues(id=int):
    session = SessionMaker()
    db_member = session.query(BookMembersModel).filter_by(id=id).first()
    session.close()
    if db_member is None:
        raise ResponseExecption(status=404, message="Book Member not Found")
    if db_member.rent_paid is True:
        raise ResponseExecption(status=400, message="Rent already paid for this member")
    db_member.rent_paid = True
    db_member.rent_paid_at = datetime.now()
    session.commit()
    session.close()


