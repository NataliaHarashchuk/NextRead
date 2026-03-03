from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from app.models.borrowing import BorrowingStatus

from app.schemas.user import UserInBorrowing
from app.schemas.book import BookInBorrowing


class BorrowingBase(BaseModel):
    book_id: str
    borrow_date: date


class BorrowingCreate(BorrowingBase):
    pass


class BorrowingUpdate(BaseModel):
    return_date: Optional[date] = None
    status: Optional[BorrowingStatus] = None


class BorrowingInDB(BaseModel):
    id: str
    user_id: str
    book_id: str
    borrow_date: date
    return_date: Optional[date] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class BorrowingWithDetails(BorrowingInDB):
    user: Optional[UserInBorrowing] = None
    book: Optional[BookInBorrowing] = None


class Borrowing(BorrowingWithDetails):
    pass