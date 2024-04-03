from array import array


class FrappeBookDto:
    def __init__(self, frappe_book):
        self.bookID = frappe_book.get('bookID', 0)  # Get bookID from frappe_book, default to empty string if not found
        self.title = frappe_book.get('title', '')  # Get title from frappe_book, default to empty string if not found
        self.authors = frappe_book.get('authors', array('i'))  # Get authors from frappe_book, default to empty array if not found
        self.average_rating = frappe_book.get('average_rating', 0.0)  # Get average_rating from frappe_book, default to 0.0 if not found
        self.isbn = frappe_book.get('isbn', 0)  # Get isbn from frappe_book, default to empty string if not found
        self.isbn13 = frappe_book.get('isbn13', 0)  # Get isbn13 from frappe_book, default to empty string if not found
        self.language_code = frappe_book.get('language_code', '')  # Get language_code_id from frappe_book, default to empty string if not found
        self.ratings_count = frappe_book.get('ratings_count', 0)  # Get ratings_count from frappe_book, default to empty string if not found
        self.num_pages = frappe_book.get('  num_pages', 0)  # Get num_pages from frappe_book, default to empty string if not found
        self.text_reviews_count = frappe_book.get('text_reviews_count', 0)  # Get text_reviews_count from frappe_book, default to empty string if not found
        self.publication_date = frappe_book.get('publication_date', None)  # Get publication_date from frappe_book, default to empty string if not found
        self.publisher = frappe_book.get('publisher', '')  # Get publisher from frappe_book, default to empty string if not found
        self.publisher_name = frappe_book.get('publisher_name', '')  # Get publisher_name from frappe_book, default to empty string if not found
        self.stock_amount = frappe_book.get('stock_amount', 0)
