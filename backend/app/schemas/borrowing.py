from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.borrowing import BorrowingStatus


class BorrowingBase(BaseModel):
    book_id: int
    borrow_date: date


class BorrowingCreate(BorrowingBase):
    pass


class BorrowingUpdate(BaseModel):
    return_date: Optional[date] = None
    status: Optional[BorrowingStatus] = None


class BorrowingInDB(BorrowingBase):
    id: int
    user_id: int
    return_date: Optional[date] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class Borrowing(BorrowingInDB):
    pass


class BorrowingWithDetails(Borrowing):
    user_username: Optional[str] = None
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    book_isbn: Optional[str] = None