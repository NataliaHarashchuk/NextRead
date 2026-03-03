from typing import Annotated
from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    hashed_password: str
    full_name: Optional[str] = None
    role: str = UserRole.USER
    is_active: bool = True
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"