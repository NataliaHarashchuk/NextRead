from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=2100)
    quantity: int = Field(default=1, ge=1)
    tags: List[str] = Field(default=[], description="Список тегів книги")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=2100)
    quantity: Optional[int] = Field(None, ge=0)
    available: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = Field(None, description="Список тегів книги")


class BookInDB(BookBase):
    id: str
    available: int
    created_at: datetime

    class Config:
        from_attributes = True


class Book(BookInDB):
    pass


class BookInBorrowing(BaseModel):
    id: str
    title: str
    author: str
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    quantity: int
    available: int
    tags: List[str] = []

    class Config:
        from_attributes = True