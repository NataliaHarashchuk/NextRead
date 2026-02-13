from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.endpoints import auth, users, books, borrowings
from app.models import User, Book, Borrowing

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="""
    ## Library System for Managing Books and Borrowings
    
    ### Features:
    
    * **Authentication** - user registration and login
    * **User Management** - CRUD operations (admin only)
    * **Book Management** - full CRUD for book catalog
    * **Borrowing Management** - borrow and return books
    
    ### User Roles:
    
    * **admin** - full access to all operations
    * **user** - limited access (view books, manage own borrowings)
    
    ### Authentication:
    
    The system uses JWT tokens. To access protected endpoints:
    1. Register via `/auth/register`
    2. Login via `/auth/login` and get token
    3. Click 'Authorize' button at the top and paste the token
    
    ### Creating First Admin:
    
    On first run, you need to create an admin manually through the database
    or change user role after registration.
    """,
    version="1.0.0",
    contact={
        "name": "Developer",
        "email": "admin@library.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Registration and login operations",
        },
        {
            "name": "Users",
            "description": "User management",
        },
        {
            "name": "Books",
            "description": "Book catalog management - full CRUD",
        },
        {
            "name": "Borrowings",
            "description": "Book borrowing management - borrow and return",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrowings.router)


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="API health check"
)
def read_root():
    """API root endpoint"""
    return {
        "message": "Welcome to the Library Management System!",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get(
    "/health",
    tags=["Root"],
    summary="Health check",
    description="Check server health"
)
def health_check():
    """System health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
