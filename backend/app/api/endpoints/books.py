from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from app.database import get_db
from app.schemas.book import Book, BookCreate, BookUpdate
from app.crud import book as book_crud
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/books", tags=["Books"])


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create new book",
    description="Add a new book to the library (admin only)"
)
def create_book(
    book: BookCreate,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Create new book (admin only)"""
    if book.isbn:
        db_book = book_crud.get_book_by_isbn(db, isbn=book.isbn)
        if db_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )
    
    return book_crud.create_book(db=db, book=book)


@router.get(
    "/",
    response_model=List[Book],
    summary="Get list of books",
    description="Get list of all books with optional search"
)
def read_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search by title or author"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Get list of books"""
    books = book_crud.get_books(db, skip=skip, limit=limit, search=search)
    return books


@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Get book by ID",
    description="Get detailed book information by ID"
)
def read_book(
    book_id: int,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Get book by ID"""
    db_book = book_crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book


@router.put(
    "/{book_id}",
    response_model=Book,
    summary="Update book",
    description="Update book information (admin only)"
)
def update_book(
    book_id: int,
    book: BookUpdate,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Update book (admin only)"""
    if book.isbn:
        existing_book = book_crud.get_book_by_isbn(db, isbn=book.isbn)
        if existing_book and existing_book.id != book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )
    
    db_book = book_crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete book",
    description="Delete book from the library (admin only)"
)
def delete_book(
    book_id: int,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Delete book (admin only)"""
    success = book_crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return None
