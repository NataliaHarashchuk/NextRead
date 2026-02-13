from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from datetime import date
from app.database import get_db
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
    summary="Borrow a book",
    description="Create new borrowing - borrow a book from the library"
)
def create_borrowing(
    borrowing: BorrowingCreate,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Borrow a book"""
    db_borrowing = borrowing_crud.create_borrowing(
        db=db, 
        borrowing=borrowing, 
        user_id=current_user.id
    )
    if db_borrowing is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available or does not exist"
        )
    return db_borrowing


@router.get(
    "/",
    response_model=List[Borrowing],
    summary="Get list of borrowings",
    description="Get list of borrowings. Admin sees all, user sees only their own"
)
def read_borrowings(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[BorrowingStatus] = Query(None, alias="status", description="Filter by status"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Get list of borrowings"""
    user_id = None if current_user.role == "admin" else current_user.id
    
    borrowings = borrowing_crud.get_borrowings(
        db, 
        skip=skip, 
        limit=limit, 
        user_id=user_id,
        status=status_filter
    )
    return borrowings


@router.get(
    "/my",
    response_model=List[Borrowing],
    summary="My borrowings",
    description="Get list of borrowings for current user"
)
def read_my_borrowings(
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Get my borrowings"""
    borrowings = borrowing_crud.get_borrowings(
        db, 
        skip=skip, 
        limit=limit, 
        user_id=current_user.id
    )
    return borrowings


@router.get(
    "/{borrowing_id}",
    response_model=Borrowing,
    summary="Get borrowing by ID",
    description="Get detailed borrowing information"
)
def read_borrowing(
    borrowing_id: int,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Get borrowing by ID"""
    db_borrowing = borrowing_crud.get_borrowing(db, borrowing_id=borrowing_id)
    if db_borrowing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrowing not found"
        )

    if current_user.role != "admin" and db_borrowing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    
    return db_borrowing


@router.put(
    "/{borrowing_id}",
    response_model=Borrowing,
    summary="Update borrowing",
    description="Update borrowing - return book or change return date"
)
def update_borrowing(
    borrowing_id: int,
    borrowing: BorrowingUpdate,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """Update borrowing (return book)"""
    db_borrowing = borrowing_crud.get_borrowing(db, borrowing_id=borrowing_id)
    if db_borrowing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrowing not found"
        )

    if current_user.role != "admin" and db_borrowing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    
    updated_borrowing = borrowing_crud.update_borrowing(
        db, 
        borrowing_id=borrowing_id, 
        borrowing=borrowing
    )
    return updated_borrowing


@router.delete(
    "/{borrowing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete borrowing",
    description="Delete borrowing record (admin only)"
)
def delete_borrowing(
    borrowing_id: int,
    current_user: Annotated[User, Depends(get_current_admin)] = None,
    db: Session = Depends(get_db)
):
    """Delete borrowing (admin only)"""
    success = borrowing_crud.delete_borrowing(db, borrowing_id=borrowing_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrowing not found"
        )
    return None
