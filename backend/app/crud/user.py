from typing import Optional, List
from beanie import PydanticObjectId
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


async def get_user(user_id: str) -> Optional[User]:
    """Get user by ID"""
    try:
        return await User.get(PydanticObjectId(user_id))
    except Exception:
        return None


async def get_user_by_username(username: str) -> Optional[User]:
    """Get user by username"""
    return await User.find_one(User.username == username)


async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email"""
    return await User.find_one(User.email == email)


async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users"""
    return await User.find_all().skip(skip).limit(limit).to_list()


async def create_user(user: UserCreate) -> User:
    """Create new user"""
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role,
    )
    await db_user.insert()
    return db_user


async def update_user(user_id: str, user: UserUpdate) -> Optional[User]:
    """Update user data"""
    db_user = await get_user(user_id)
    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    await db_user.set(update_data)
    return await get_user(user_id)


async def delete_user(user_id: str) -> bool:
    """Delete user"""
    db_user = await get_user(user_id)
    if not db_user:
        return False
    await db_user.delete()
    return True