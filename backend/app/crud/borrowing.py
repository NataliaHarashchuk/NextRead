from typing import Optional, List
from beanie import PydanticObjectId
from app.models.borrowing import Borrowing, BorrowingStatus
from app.models.book import Book
from app.models.user import User
from app.schemas.borrowing import BorrowingCreate, BorrowingUpdate


async def _enrich(borrowing: Borrowing) -> dict:
    """Fetch related user and book documents and return enriched dict"""
    user = await User.get(borrowing.user_id)
    book = await Book.get(borrowing.book_id)

    data = borrowing.model_dump()
    data["id"] = str(borrowing.id)
    data["user_id"] = str(borrowing.user_id)
    data["book_id"] = str(borrowing.book_id)

    if user:
        data["user"] = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
        }

    if book:
        data["book"] = {
            "id": str(book.id),
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "published_year": book.published_year,
            "quantity": book.quantity,
            "available": book.available,
            "tags": book.tags or [],
        }

    return data


async def get_borrowing(borrowing_id: str) -> Optional[dict]:
    """Get borrowing by ID with user and book details"""
    try:
        borrowing = await Borrowing.get(PydanticObjectId(borrowing_id))
    except Exception:
        return None
    if not borrowing:
        return None
    return await _enrich(borrowing)


async def get_borrowings(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[str] = None,
    status: Optional[str] = None,
) -> List[dict]:
    """Get list of borrowings with optional filters"""
    filters = {}
    if user_id:
        filters["user_id"] = PydanticObjectId(user_id)
    if status:
        filters["status"] = status

    borrowings = await Borrowing.find(filters).skip(skip).limit(limit).to_list()
    return [await _enrich(b) for b in borrowings]


async def create_borrowing(borrowing: BorrowingCreate, user_id: str) -> Optional[dict]:
    """Borrow a book"""
    try:
        book = await Book.get(PydanticObjectId(borrowing.book_id))
    except Exception:
        return None

    if not book or book.available <= 0:
        return None

    db_borrowing = Borrowing(
        user_id=PydanticObjectId(user_id),
        book_id=PydanticObjectId(borrowing.book_id),
        borrow_date=borrowing.borrow_date,
        status=BorrowingStatus.BORROWED,
    )
    await db_borrowing.insert()
    await book.set({"available": book.available - 1})

    return await get_borrowing(str(db_borrowing.id))


async def update_borrowing(borrowing_id: str, borrowing: BorrowingUpdate) -> Optional[dict]:
    """Update borrowing (e.g. return book)"""
    try:
        db_borrowing = await Borrowing.get(PydanticObjectId(borrowing_id))
    except Exception:
        return None
    if not db_borrowing:
        return None

    update_data = borrowing.model_dump(exclude_unset=True)

    if update_data.get("status") == BorrowingStatus.RETURNED:
        if db_borrowing.status != BorrowingStatus.RETURNED:
            book = await Book.get(db_borrowing.book_id)
            if book:
                await book.set({"available": book.available + 1})

    await db_borrowing.set(update_data)
    return await get_borrowing(borrowing_id)


async def delete_borrowing(borrowing_id: str) -> bool:
    """Delete borrowing record"""
    try:
        db_borrowing = await Borrowing.get(PydanticObjectId(borrowing_id))
    except Exception:
        return False
    if not db_borrowing:
        return False

    if db_borrowing.status == BorrowingStatus.BORROWED:
        book = await Book.get(db_borrowing.book_id)
        if book:
            await book.set({"available": book.available + 1})

    await db_borrowing.delete()
    return True