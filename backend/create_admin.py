"""
Script to create first admin in the system
Usage: python create_admin.py
"""

from app.database import SessionLocal
from app.crud import user as user_crud
from app.schemas.user import UserCreate

def create_admin():
    db = SessionLocal()
    
    try:
        existing_admin = user_crud.get_user_by_username(db, username="admin")
        if existing_admin:
            print("Admin with username 'admin' already exists!")
            return

        admin_data = UserCreate(
            username="admin",
            email="admin@library.com",
            password="admin123",
            full_name="System Administrator",
            role="admin"
        )
        
        admin = user_crud.create_user(db, admin_data)
        print(f"Successfully created admin!")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"\nWARNING: Change password after first login!")
        
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating system administrator...\n")
    create_admin()
