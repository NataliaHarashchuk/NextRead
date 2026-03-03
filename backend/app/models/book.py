from typing import Annotated, List, Optional
from beanie import Document, Indexed
from datetime import datetime


class Book(Document):
    title: str
    author: str
    isbn: Annotated[Optional[str], Indexed(unique=True)] = None
    published_year: Optional[int] = None
    quantity: int = 1
    available: int = 1
    tags: List[str] = []
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "books"