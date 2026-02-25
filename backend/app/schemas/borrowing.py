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


from app.schemas.user import UserInBorrowing
from app.schemas.book import BookInBorrowing


class Borrowing(BorrowingInDB):
    user: UserInBorrowing
    book: BookInBorrowing


class BorrowingWithDetails(Borrowing):
    pass