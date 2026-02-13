from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from app.models.borrowing import Borrowing, BorrowingStatus
from app.models.book import Book
from app.schemas.borrowing import BorrowingCreate, BorrowingUpdate


def get_borrowing(db: Session, borrowing_id: int) -> Optional[Borrowing]:
    """Get borrowing by ID"""
    return db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()


def get_borrowings(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Borrowing]:
    """Get list of borrowings with filtering"""
    query = db.query(Borrowing)
    
    if user_id:
        query = query.filter(Borrowing.user_id == user_id)
    if status:
        query = query.filter(Borrowing.status == status)
    
    return query.offset(skip).limit(limit).all()


def create_borrowing(
    db: Session, 
    borrowing: BorrowingCreate, 
    user_id: int
) -> Optional[Borrowing]:
    """Create new borrowing (borrow a book)"""
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book or book.available <= 0:
        return None

    db_borrowing = Borrowing(
        user_id=user_id,
        book_id=borrowing.book_id,
        borrow_date=borrowing.borrow_date,
        status=BorrowingStatus.BORROWED
    )

    book.available -= 1
    
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def update_borrowing(
    db: Session, 
    borrowing_id: int, 
    borrowing: BorrowingUpdate
) -> Optional[Borrowing]:
    """Update borrowing (return book)"""
    db_borrowing = get_borrowing(db, borrowing_id)
    if not db_borrowing:
        return None
    
    update_data = borrowing.model_dump(exclude_unset=True)

    if "status" in update_data and update_data["status"] == BorrowingStatus.RETURNED:
        if db_borrowing.status != BorrowingStatus.RETURNED:
            book = db.query(Book).filter(Book.id == db_borrowing.book_id).first()
            if book:
                book.available += 1
    
    for key, value in update_data.items():
        setattr(db_borrowing, key, value)
    
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def delete_borrowing(db: Session, borrowing_id: int) -> bool:
    """Delete borrowing"""
    db_borrowing = get_borrowing(db, borrowing_id)
    if not db_borrowing:
        return False

    if db_borrowing.status == BorrowingStatus.BORROWED:
        book = db.query(Book).filter(Book.id == db_borrowing.book_id).first()
        if book:
            book.available += 1
    
    db.delete(db_borrowing)
    db.commit()
    return True
