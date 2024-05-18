from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text, and_
from connections.db import engine

SessionMaker = sessionmaker(bind=engine)

def get_book_stats():
    session = SessionMaker()
    query = text(f'SELECT books.id, books.title, books.stock_amount, COUNT(book_members.*) as book_members_count FROM books INNER JOIN book_members ON books.id =  book_members.book_id GROUP BY books.id, book_members.id')

    results = session.execute(query).fetchall()
    session.close()
    results_dict = [
        {"id": row.id, "title": row.title, "stock_amount": row.stock_amount, "book_members_count": row.book_members_count}
        for row in results
    ]

    return results_dict
    

def member_wise_rent_stats():
    session = SessionMaker()
    query = text(f'SELECT COUNT(*) as count, SUM(bm.price) as total_price,  m.id, m.first_name, m.last_name  from members m INNER JOIN book_members bm ON bm.member_id = m.id  WHERE bm.rent_paid = true GROUP BY m.id, m.first_name, m.last_name')
    result_rent_paid = session.execute(query).fetchall()
    results_rent_paid_dict = [
        { "count": row.count, "price": row.total_price, "id": row.id, "name": f"{row.first_name} {row.last_name}"}
        for row in result_rent_paid
    ]
    query = text(f'SELECT COUNT(*) as count, SUM(bm.price) as total_price,  m.id, m.first_name, m.last_name  from members m INNER JOIN book_members bm ON bm.member_id = m.id  GROUP BY m.id, m.first_name, m.last_name')
    result_total = session.execute(query).fetchall()
    results_total_dict = [
        { "count": row.count, "price": row.total_price, "id": row.id, "name": f"{row.first_name} {row.last_name}"}
        for row in result_total
    ]
    session.close()
    return  {
       "members_rent_paid_stats": results_rent_paid_dict,
       "members_stats": results_total_dict,
    }



