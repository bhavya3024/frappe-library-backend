import sys
from fastapi import FastAPI
sys.path.append('./routes/frappeLibrary.py')
sys.path.append('./routes/books.py')

import routes.frappeLibrary
import routes.books
import routes.members
import routes.bookMembers

frappeLibraryRoute = routes.frappeLibrary
booksRoute = routes.books
membersRoute = routes.members
bookMembersRoute = routes.bookMembers


app = FastAPI()

app.include_router(frappeLibraryRoute.router, prefix="/frappe-libraries")

app.include_router(booksRoute.router, prefix="/books")

app.include_router(membersRoute.router, prefix='/members')

app.include_router(bookMembersRoute.router, prefix='/book-members')