from typing import Optional, List
from beanie import PydanticObjectId
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


async def get_book(book_id: str) -> Optional[Book]:
    """Get book by ID"""
    try:
        return await Book.get(PydanticObjectId(book_id))
    except Exception:
        return None


async def get_book_by_isbn(isbn: str) -> Optional[Book]:
    """Get book by ISBN"""
    return await Book.find_one(Book.isbn == isbn)


async def get_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> List[Book]:
    filter_clauses = []

    if search:
        terms = search.strip().split()
        for term in terms:
            filter_clauses.append({
                "$or": [
                    {"title":  {"$regex": term, "$options": "i"}},
                    {"author": {"$regex": term, "$options": "i"}},
                ]
            })

    if tags:
        for tag in tags:
            filter_clauses.append({
                "tags": {"$elemMatch": {"$regex": tag, "$options": "i"}}
            })

    query = Book.find({"$and": filter_clauses}) if filter_clauses else Book.find_all()
    return await query.skip(skip).limit(limit).to_list()


async def get_all_tags() -> List[str]:
    """Return sorted list of all unique tags across all books.

    Uses the Motor collection directly (via Beanie's get_settings().motor_db)
    because Beanie's aggregate() wrapper does not support async-for iteration
    in all versions.
    """
    from app.database import client
    from app.config import settings

    pipeline = [
        {"$unwind": "$tags"},
        {"$group":  {"_id": "$tags"}},
        {"$sort":   {"_id": 1}},
    ]

    motor_collection = client[settings.MONGODB_DB]["books"]
    result = []
    async for doc in motor_collection.aggregate(pipeline):
        result.append(doc["_id"])
    return result


async def create_book(book: BookCreate) -> Book:
    """Create new book"""
    db_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn if book.isbn else None,
        published_year=book.published_year,
        quantity=book.quantity,
        available=book.quantity,
        tags=[t.strip().lower() for t in book.tags if t.strip()],
    )
    await db_book.insert()
    return db_book


async def update_book(book_id: str, book: BookUpdate) -> Optional[Book]:
    """Update book data"""
    db_book = await get_book(book_id)
    if not db_book:
        return None

    update_data = book.model_dump(exclude_unset=True)

    if "isbn" in update_data and not update_data["isbn"]:
        update_data["isbn"] = None

    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = [t.strip().lower() for t in update_data["tags"] if t.strip()]

    await db_book.set(update_data)
    return await get_book(book_id)


async def delete_book(book_id: str) -> bool:
    """Delete book"""
    db_book = await get_book(book_id)
    if not db_book:
        return False
    await db_book.delete()
    return True