from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database import get_db
from app.schemas.user import User, UserUpdate
from app.crud import user as user_crud
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=User,
    summary="Get current user",
    description="Get information about authenticated user"
)
def read_current_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Get current user information"""
    return current_user


@router.get(
    "/",
    response_model=List[User],
    summary="Get list of users",
    description="Get list of all users (admin only)"
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Get list of users (admin only)"""
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Get user information by ID (admin only)"
)
def read_user(
    user_id: int,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)"""
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=User,
    summary="Update user",
    description="Update user information (admin only)"
)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Update user (admin only)"""
    db_user = user_crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete user from the system (admin only)"
)
def delete_user(
    user_id: int,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    success = user_crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None
