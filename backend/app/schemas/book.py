from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=2100)
    quantity: int = Field(default=1, ge=1)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=2100)
    quantity: Optional[int] = Field(None, ge=0)
    available: Optional[int] = Field(None, ge=0)


class BookInDB(BookBase):
    id: int
    available: int
    created_at: datetime

    class Config:
        from_attributes = True


class Book(BookInDB):
    pass
