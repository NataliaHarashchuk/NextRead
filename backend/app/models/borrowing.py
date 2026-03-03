from beanie import Document, PydanticObjectId
from typing import Optional
from datetime import datetime, date
import enum


class BorrowingStatus(str, enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"


class Borrowing(Document):
    user_id: PydanticObjectId
    book_id: PydanticObjectId
    borrow_date: date
    return_date: Optional[date] = None
    status: str = BorrowingStatus.BORROWED
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "borrowings"