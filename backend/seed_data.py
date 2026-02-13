"""
Script to populate database with test data
Usage: python seed_data.py
"""

from datetime import date, timedelta
from app.database import SessionLocal
from app.crud import user as user_crud, book as book_crud, borrowing as borrowing_crud
from app.schemas.user import UserCreate
from app.schemas.book import BookCreate
from app.schemas.borrowing import BorrowingCreate

def seed_database():
    db = SessionLocal()
    
    try:
        print("Seeding database with test data...\n")

        print("Creating users...")
        users_data = [
            UserCreate(
                username="admin",
                email="admin@library.com",
                password="admin123",
                full_name="System Administrator",
                role="admin"
            ),
            UserCreate(
                username="user1",
                email="user1@example.com",
                password="user123",
                full_name="John Doe",
                role="user"
            ),
            UserCreate(
                username="user2",
                email="user2@example.com",
                password="user123",
                full_name="Jane Smith",
                role="user"
            ),
        ]
        
        created_users = []
        for user_data in users_data:
            existing = user_crud.get_user_by_username(db, user_data.username)
            if not existing:
                user = user_crud.create_user(db, user_data)
                created_users.append(user)
                print(f"   Created: {user.username} ({user.role})")
            else:
                created_users.append(existing)
                print(f"   Already exists: {user_data.username}")

        print("\nCreating books...")
        books_data = [
            BookCreate(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                isbn="978-0-06-112008-4",
                published_year=1960,
                quantity=5
            ),
            BookCreate(
                title="1984",
                author="George Orwell",
                isbn="978-0-452-28423-4",
                published_year=1949,
                quantity=3
            ),
            BookCreate(
                title="Pride and Prejudice",
                author="Jane Austen",
                isbn="978-0-14-143951-8",
                published_year=1813,
                quantity=4
            ),
            BookCreate(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                isbn="978-0-7432-7356-5",
                published_year=1925,
                quantity=2
            ),
            BookCreate(
                title="Harry Potter and the Philosopher's Stone",
                author="J.K. Rowling",
                isbn="978-0-7475-3269-9",
                published_year=1997,
                quantity=6
            ),
            BookCreate(
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                isbn="978-0-316-76948-0",
                published_year=1951,
                quantity=3
            ),
            BookCreate(
                title="The Lord of the Rings",
                author="J.R.R. Tolkien",
                isbn="978-0-618-00222-1",
                published_year=1954,
                quantity=4
            ),
        ]
        
        created_books = []
        for book_data in books_data:
            existing = book_crud.get_book_by_isbn(db, book_data.isbn) if book_data.isbn else None
            if not existing:
                book = book_crud.create_book(db, book_data)
                created_books.append(book)
                print(f"   Added: {book.title} - {book.author}")
            else:
                created_books.append(existing)
                print(f"   Already exists: {book_data.title}")

        print("\nCreating test borrowings...")
        if len(created_users) >= 2 and len(created_books) >= 3:
            borrowings_data = [
                BorrowingCreate(
                    book_id=created_books[0].id,
                    borrow_date=date.today() - timedelta(days=7)
                ),
                BorrowingCreate(
                    book_id=created_books[1].id,
                    borrow_date=date.today() - timedelta(days=20)
                ),
                BorrowingCreate(
                    book_id=created_books[2].id,
                    borrow_date=date.today() - timedelta(days=3)
                ),
            ]

            if created_users[1]:
                borrowing1 = borrowing_crud.create_borrowing(
                    db, borrowings_data[0], user_id=created_users[1].id
                )
                if borrowing1:
                    print(f"   {created_users[1].username} borrowed: {created_books[0].title}")
                
                borrowing2 = borrowing_crud.create_borrowing(
                    db, borrowings_data[1], user_id=created_users[1].id
                )
                if borrowing2:
                    from app.schemas.borrowing import BorrowingUpdate
                    from app.models.borrowing import BorrowingStatus
                    update_data = BorrowingUpdate(
                        return_date=date.today() - timedelta(days=10),
                        status=BorrowingStatus.RETURNED
                    )
                    borrowing_crud.update_borrowing(db, borrowing2.id, update_data)
                    print(f"   {created_users[1].username} returned: {created_books[1].title}")

            if len(created_users) > 2 and created_users[2]:
                borrowing3 = borrowing_crud.create_borrowing(
                    db, borrowings_data[2], user_id=created_users[2].id
                )
                if borrowing3:
                    print(f"   {created_users[2].username} borrowed: {created_books[2].title}")
        
        print("\nDatabase successfully seeded with test data!")
        print("\nStatistics:")
        print(f"   Users: {len(created_users)}")
        print(f"   Books: {len(created_books)}")
        print(f"   Borrowings: 3")
        
        print("\nLogin credentials:")
        print("   Administrator:")
        print("     username: admin")
        print("     password: admin123")
        print("   User 1:")
        print("     username: user1")
        print("     password: user123")
        print("   User 2:")
        print("     username: user2")
        print("     password: user123")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
