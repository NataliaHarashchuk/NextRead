from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings

client: AsyncIOMotorClient | None = None


async def connect_db():
    """Connect to MongoDB and initialize Beanie ODM"""
    global client
    from app.models.user import User
    from app.models.book import Book
    from app.models.borrowing import Borrowing

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB]

    await init_beanie(
        database=db,
        document_models=[User, Book, Borrowing]
    )
    print(f"Connected to MongoDB: {settings.MONGODB_DB}")


async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")