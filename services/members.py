from models.membersDto import MembersDto
from models.members import MembersModel
from models.books import BookModel
from models.bookMembers import BookMembersModel
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from connections.db import engine
from utils.index import ResponseExecption, convert_query_result_to_json
from sqlalchemy import text




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
    session.close()
    return members


def get_members_count():
    session = Session()
    members_count = session.query(MembersModel).filter().count()
    session.close()
    return members_count


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


def get_books_by_member_id(id:int, page:int):
    session = Session()
    results = session.execute(text('''
    select b.*, bm.rent_start_date, bm.rent_end_date, bm.rent_paid from members m  inner join book_members bm ON  m.id = bm.member_id inner join books b on bm.book_id  = b.id where m.id = :id LIMIT 10 OFFSET ((:page - 1) * 10);
    '''), {
        "id": id,
        "page": page
    })
    books = results.fetchall()
    books_json = convert_query_result_to_json(results, books)
    session.close()
    return books_json


def get_books_count(id:int):
    session = Session()
    results = session.execute(text('''
    select count(*) from members m  inner join book_members bm ON  m.id = bm.member_id inner join books b on bm.book_id  = b.id where m.id = :id;
    '''), {
        "id": id,
    })
    rows = results.fetchall()
    return rows[0][0]



def get_member_by_id(id=int):
    session = Session()
    db_member = session.query(MembersModel).filter_by(id=id).first()
    session.close()
    if db_member is None:
        raise ResponseExecption(status=404, message="Member not Found")
    return db_member

def get_member_pending_dues(id=int):
    session = Session()
    results = session.execute(text('''
       select sum(price) from members inner join book_members on book_members.member_id = members.id inner join books on books.id = book_members.book_id
       WHERE members.id = :id AND book_members.rent_paid = false;
    '''), {
        "id": id
    })
    rows = results.fetchall()
    return rows[0][0]


def delete_member(id=int):
    session = Session()
    session.query(MembersModel).delete(id=id)
    session.commit()
    session.close()




