from sqlalchemy import Column, Integer, String, DateTime,Index,func, literal_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func as sql_func
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    published_year = Column(Integer)
    quantity = Column(Integer, default=1)
    available = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=sql_func.now())

    borrowings = relationship("Borrowing", back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (
        Index(
            'ix_book_search_vector',
            func.to_tsvector(literal_column("'simple'"), title + ' ' + author),
            postgresql_using='gin'
        ),
    )