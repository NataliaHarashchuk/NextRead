from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.api.endpoints import auth, users, books, borrowings
from app.models import user, book, borrowing
from app.config import settings

from migrate_sqlite_to_postgres import migrate_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    yield
    print("Application is shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## Library System for Managing Books and Borrowings
    
    ### Features:
    
    * **Authentication** - user registration and login with JWT
    * **User Management** - CRUD operations (admin only)
    * **Book Management** - full CRUD for book catalog
    * **Borrowing Management** - borrow and return books
    * **PostgreSQL Backend** - reliable and scalable database
    
    ### User Roles:
    
    * **admin** - full access to all operations
    * **user** - limited access (view books, manage own borrowings)
    
    ### Authentication:
    
    The system uses JWT tokens. To access protected endpoints:
    1. Register via `/auth/register`
    2. Login via `/auth/login` and get token
    3. Click 'Authorize' button at the top and paste the token
    
    ### Database:
    
    This application uses PostgreSQL for data persistence.
    """,
    version=settings.VERSION,
    lifespan=lifespan,
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

if settings.CORS_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
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
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "docs": "/docs",
        "version": settings.VERSION,
        "database": "PostgreSQL"
    }


@app.get(
    "/health",
    tags=["Root"],
    summary="Health check",
    description="Check server and database health"
)
def health_check():
    """System health check"""
    try:
        # Перевірка підключення до БД
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.VERSION
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )