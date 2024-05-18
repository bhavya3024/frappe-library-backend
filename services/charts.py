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
    
def get_total_members():
    session = SessionMaker()
    query = text(f'SELECT COUNT(*) FROM members')

    results = session.execute(query).fetchall()
    session.close()
    return {
      "total_members":  results[0][0]
    }


def get_total_book_purchases_vs_rent_paid():
    session = SessionMaker()
    query = text(f'SELECT COUNT(*) FROM book_members WHERE rent_paid = false')
    result_not_paid = session.execute(query).fetchall()
    
    query = text(f"SELECT COUNT(*) FROM book_members")
    result_total = session.execute(query).fetchall()
    session.close()
    return {
        "total_book_purchases": result_not_paid[0][0],
        "rent_paid": result_total[0][0]
    }



