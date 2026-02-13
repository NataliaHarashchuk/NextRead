from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Get book by ID"""
    return db.query(Book).filter(Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    """Get book by ISBN"""
    return db.query(Book).filter(Book.isbn == isbn).first()


def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None
) -> List[Book]:
    """Get list of books with optional search"""
    query = db.query(Book)
    
    if search:
        query = query.filter(
            (Book.title.contains(search)) | 
            (Book.author.contains(search))
        )
    
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> Book:
    """Create new book"""
    db_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        published_year=book.published_year,
        quantity=book.quantity,
        available=book.quantity
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    """Update book data"""
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    update_data = book.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """Delete book"""
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    
    db.delete(db_book)
    db.commit()
    return True
