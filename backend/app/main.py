from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import connect_db, close_db
from app.api.endpoints import auth, users, books, borrowings
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    print("Application is starting...")
    yield
    await close_db()
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
    * **MongoDB Backend** - flexible and scalable NoSQL database

    ### User Roles:

    * **admin** - full access to all operations
    * **user** - limited access (view books, manage own borrowings)

    ### Authentication:

    The system uses JWT tokens. To access protected endpoints:
    1. Register via `/auth/register`
    2. Login via `/auth/login` and get token
    3. Click 'Authorize' button at the top and paste the token
    """,
    version=settings.VERSION,
    lifespan=lifespan,
    contact={"name": "Developer", "email": "admin@library.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "Authentication", "description": "Registration and login operations"},
        {"name": "Users", "description": "User management"},
        {"name": "Books", "description": "Book catalog management - full CRUD"},
        {"name": "Borrowings", "description": "Book borrowing management - borrow and return"},
    ],
)

origins = ["*"] if settings.CORS_ORIGINS == "*" else [
    o.strip() for o in settings.CORS_ORIGINS.split(",")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrowings.router)


@app.get("/", tags=["Root"], summary="Root endpoint")
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "docs": "/docs",
        "version": settings.VERSION,
        "database": "MongoDB",
    }


@app.get("/health", tags=["Root"], summary="Health check")
async def health_check():
    from app.database import client as db_client
    if db_client is None:
        return {"status": "unhealthy", "database": "not initialized", "version": settings.VERSION}
    try:
        await db_client.admin.command("ping")
        return {"status": "healthy", "database": "connected", "version": settings.VERSION}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)