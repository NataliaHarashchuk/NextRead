from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Annotated
from app.schemas.borrowing import Borrowing, BorrowingCreate, BorrowingUpdate, BorrowingWithDetails
from app.crud import borrowing as borrowing_crud
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User
from app.models.borrowing import BorrowingStatus

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])


@router.post(
    "/",
    response_model=Borrowing,
    status_code=status.HTTP_201_CREATED,
    summary="Borrow a book"
)
async def create_borrowing(
    borrowing: BorrowingCreate,
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    result = await borrowing_crud.create_borrowing(borrowing, user_id=str(current_user.id))
    if not result:
        raise HTTPException(status_code=400, detail="Book is not available or does not exist")
    return result


@router.get(
    "/",
    response_model=List[Borrowing],
    summary="Get list of borrowings (admin sees all, user sees own)"
)
async def read_borrowings(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[BorrowingStatus] = Query(None, alias="status"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    user_id = None if current_user.role == "admin" else str(current_user.id)
    return await borrowing_crud.get_borrowings(
        skip=skip, limit=limit, user_id=user_id, status=status_filter
    )


@router.get(
    "/my",
    response_model=List[BorrowingWithDetails],
    summary="My borrowings"
)
async def read_my_borrowings(
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    return await borrowing_crud.get_borrowings(
        skip=skip, limit=limit, user_id=str(current_user.id)
    )


@router.get("/{borrowing_id}", response_model=Borrowing, summary="Get borrowing by ID")
async def read_borrowing(
    borrowing_id: str,
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    db_borrowing = await borrowing_crud.get_borrowing(borrowing_id)
    if not db_borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    if current_user.role != "admin" and db_borrowing["user_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="Access forbidden")

    return db_borrowing


@router.put("/{borrowing_id}", response_model=Borrowing, summary="Update borrowing / return book")
async def update_borrowing(
    borrowing_id: str,
    borrowing: BorrowingUpdate,
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    db_borrowing = await borrowing_crud.get_borrowing(borrowing_id)
    if not db_borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    if current_user.role != "admin" and db_borrowing["user_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="Access forbidden")

    updated = await borrowing_crud.update_borrowing(borrowing_id, borrowing)
    return updated


@router.delete(
    "/{borrowing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete borrowing (admin only)"
)
async def delete_borrowing(
    borrowing_id: str,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
):
    success = await borrowing_crud.delete_borrowing(borrowing_id)
    if not success:
        raise HTTPException(status_code=404, detail="Borrowing not found")