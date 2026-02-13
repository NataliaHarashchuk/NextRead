from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True)
    published_year = Column(Integer)
    quantity = Column(Integer, default=1)
    available = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    borrowings = relationship("Borrowing", back_populates="book", cascade="all, delete-orphan")
