import enum
from datetime import date
from sqlalchemy import (
    Column, Integer, String, Text, 
    Boolean, Date, ForeignKey, Enum, Table
)
from sqlalchemy.orm import relationship
from database import Base


book_author_association = Table(
    "book_author",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE")),
)

book_genre_association = Table(
    "book_genre",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE")),
)


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class BookItemStatus(str, enum.Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    LOST = "lost"
    DAMAGED = "damaged"

class QueueStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class NotificationType(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"

class PenaltyReason(str, enum.Enum):
    OVERDUE = "overdue"
    DAMAGE = "damage"
    LOST_ITEM = "lost_item"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    penalty_end_date = Column(Date, nullable=True)

    loans = relationship("Loan", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    queue_entries = relationship("Queue", back_populates="user")
    penalty_history = relationship("PenaltyHistory", back_populates="user")

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    
    books = relationship("Book", secondary=book_author_association, back_populates="authors")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    
    books = relationship("Book", secondary=book_genre_association, back_populates="genres")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(Integer, nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    cover_url = Column(String(255), nullable=True)

    authors = relationship("Author", secondary=book_author_association, back_populates="books")
    genres = relationship("Genre", secondary=book_genre_association, back_populates="books")
    items = relationship("BookItem", back_populates="book")
    queue = relationship("Queue", back_populates="book")

class BookItem(Base):
    __tablename__ = "book_items"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(Enum(BookItemStatus), default=BookItemStatus.AVAILABLE, nullable=False)
    
    book = relationship("Book", back_populates="items")
    loans = relationship("Loan", back_populates="book_item")

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_item_id = Column(Integer, ForeignKey("book_items.id"))
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="loans")
    book_item = relationship("BookItem", back_populates="loans")

class Queue(Base):
    __tablename__ = "queues"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    request_date = Column(Date, default=date.today, nullable=False)
    status = Column(Enum(QueueStatus), default=QueueStatus.PENDING, nullable=False)

    user = relationship("User", back_populates="queue_entries")
    book = relationship("Book", back_populates="queue")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.INFO, nullable=False)

    user = relationship("User", back_populates="notifications")

class PenaltyHistory(Base):
    __tablename__ = "penalty_histories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reason = Column(Enum(PenaltyReason), nullable=False)
    duration_days = Column(Integer, nullable=False)

    user = relationship("User", back_populates="penalty_history")