import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
sys.path.append('./routes/frappeLibrary.py')
sys.path.append('./routes/books.py')

import routes.charts
import routes.frappeLibrary
import routes.books
import routes.members
import routes.bookMembers

frappeLibraryRoute = routes.frappeLibrary
booksRoute = routes.books
membersRoute = routes.members
bookMembersRoute = routes.bookMembers
chartsRoute = routes.charts


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # Add allowed HTTP methods
    allow_headers=["*"],  # Replace "*" with your allowed headers
)




app.include_router(frappeLibraryRoute.router, prefix="/frappe-books")

app.include_router(booksRoute.router, prefix="/books")

app.include_router(membersRoute.router, prefix='/members')

app.include_router(bookMembersRoute.router, prefix='/book-members')

app.include_router(chartsRoute.router, prefix='/charts')