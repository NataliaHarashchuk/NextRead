from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Annotated
from app.schemas.book import Book, BookCreate, BookUpdate
from app.crud import book as book_crud
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/books", tags=["Books"])


def _book_to_schema(book) -> dict:
    return {
        "id": str(book.id),
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "published_year": book.published_year,
        "quantity": book.quantity,
        "available": book.available,
        "tags": book.tags or [],
        "created_at": book.created_at,
    }


@router.get(
    "/tags",
    response_model=List[str],
    summary="Get all unique tags",
    description="Returns a sorted list of all tags used across the book catalog"
)
async def get_all_tags():
    """Get all unique tags (public)"""
    return await book_crud.get_all_tags()


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create new book (admin only)"
)
async def create_book(
    book: BookCreate,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
):
    if book.isbn:
        if await book_crud.get_book_by_isbn(book.isbn):
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    db_book = await book_crud.create_book(book)
    return _book_to_schema(db_book)


@router.get(
    "/",
    response_model=List[Book],
    summary="Get list of books",
    description="Search by text (partial match in title/author) and/or filter by tags"
)
async def read_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Пошук за назвою або автором (частковий збіг)"),
    tags: Optional[List[str]] = Query(None, description="Фільтр за тегами (можна передати кілька)"),
):
    books = await book_crud.get_books(skip=skip, limit=limit, search=search, tags=tags)
    return [_book_to_schema(b) for b in books]


@router.get("/{book_id}", response_model=Book, summary="Get book by ID")
async def read_book(book_id: str):
    db_book = await book_crud.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return _book_to_schema(db_book)


@router.put("/{book_id}", response_model=Book, summary="Update book (admin only)")
async def update_book(
    book_id: str,
    book: BookUpdate,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
):
    if book.isbn:
        existing = await book_crud.get_book_by_isbn(book.isbn)
        if existing and str(existing.id) != book_id:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    db_book = await book_crud.update_book(book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return _book_to_schema(db_book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete book (admin only)")
async def delete_book(
    book_id: str,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
):
    success = await book_crud.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")