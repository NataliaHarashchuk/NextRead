from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.ext.associationproxy import association_proxy
import enum


class BorrowingStatus(str, enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String, default=BorrowingStatus.BORROWED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")

    book_title = association_proxy("book", "title")
    book_author = association_proxy("book", "author")
    book_isbn = association_proxy("book", "isbn")
    user_username = association_proxy("user", "username")