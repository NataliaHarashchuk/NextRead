from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from app.schemas.user import User, UserUpdate
from app.crud import user as user_crud
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["Users"])


def _user_to_schema(user) -> dict:
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


@router.get("/me", response_model=User, summary="Get current user")
async def read_current_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return _user_to_schema(current_user)


@router.get("/", response_model=List[User], summary="Get list of users (admin only)")
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
):
    users = await user_crud.get_users(skip=skip, limit=limit)
    return [_user_to_schema(u) for u in users]


@router.get("/{user_id}", response_model=User, summary="Get user by ID (admin only)")
async def read_user(
    user_id: str,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
):
    db_user = await user_crud.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_schema(db_user)


@router.put("/{user_id}", response_model=User, summary="Update user (admin only)")
async def update_user(
    user_id: str,
    user: UserUpdate,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
):
    db_user = await user_crud.update_user(user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_schema(db_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user (admin only)")
async def delete_user(
    user_id: str,
    current_user: Annotated[UserModel, Depends(get_current_admin)] = None,
):
    success = await user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")