"""
Script for migrating data from SQLite to PostgreSQL
"""
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.book import Book
from app.models.borrowing import Borrowing
from app.config import settings

SQLITE_DB = "library.db"

def migrate_data():
    """Data migration from SQLite to PostgreSQL"""
    
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    pg_engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=pg_engine)
    pg_session = SessionLocal()
    
    try:
        print("Starting migration from SQLite to PostgreSQL...")
        
        print("\nMigrating users...")
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        for row in users:
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                hashed_password=row['hashed_password'],
                full_name=row['full_name'],
                role=row['role'],
                is_active=row['is_active'],
                created_at=row['created_at']
            )
            pg_session.merge(user)
        
        pg_session.commit()
        print(f"Migrated {len(users)} users")


        print("\nMigrating books...")
        sqlite_cursor.execute("SELECT * FROM books")
        books = sqlite_cursor.fetchall()
        
        for row in books:
            book = Book(
                id=row['id'],
                title=row['title'],
                author=row['author'],
                isbn=row['isbn'],
                published_year=row['published_year'],
                quantity=row['quantity'],
                available=row['available'],
                created_at=row['created_at']
            )
            pg_session.merge(book)
        
        pg_session.commit()
        print(f"Migrated {len(books)} books")
        

        print("\nMigrating borrowings...")
        sqlite_cursor.execute("SELECT * FROM borrowings")
        borrowings = sqlite_cursor.fetchall()
        
        for row in borrowings:
            borrowing = Borrowing(
                id=row['id'],
                user_id=row['user_id'],
                book_id=row['book_id'],
                borrow_date=row['borrow_date'],
                return_date=row['return_date'],
                status=row['status'],
                created_at=row['created_at']
            )
            pg_session.merge(borrowing)
        
        pg_session.commit()
        print(f"Migrated {len(borrowings)} borrowings")
        
        print("\nUpdating sequences...")

        pg_session.execute(text("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))"))
        pg_session.execute(text("SELECT setval('books_id_seq', (SELECT MAX(id) FROM books))"))
        pg_session.execute(text("SELECT setval('borrowings_id_seq', (SELECT MAX(id) FROM borrowings))"))
        pg_session.commit()
        
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"\nMigration failed: {e}")
        pg_session.rollback()
        raise
    finally:
        sqlite_conn.close()
        pg_session.close()


if __name__ == "__main__":
    migrate_data()