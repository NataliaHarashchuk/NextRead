from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import User, UserCreate
from app.crud import user as user_crud
from app.core.security import verify_password, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


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


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account in the system"
)
async def register(user: UserCreate):
    if await user_crud.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await user_crud.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = await user_crud.create_user(user)
    return _user_to_schema(db_user)


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate user and get JWT token"
)
async def login(login_data: LoginRequest):
    user = await user_crud.get_user_by_username(login_data.username)

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is deactivated")

    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=expires)
    return {"access_token": token, "token_type": "bearer"}