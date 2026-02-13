# Library Management System

FastAPI Laboratory Work - Library Management System.

## Project Description

Library management system with support for:
- User registration and authentication
- Book catalog management (full CRUD)
- Book borrowing and returning
- Role-based access control (administrator / user)

## Database Structure

### Tables:

1. **users** - system users
   - id, username, email, hashed_password, full_name, role, is_active, created_at

2. **books** - book catalog
   - id, title, author, isbn, published_year, quantity, available, created_at

3. **borrowings** - book borrowings
   - id, user_id (FK), book_id (FK), borrow_date, return_date, status, created_at

### Relationships:
- User 1:N Borrowing
- Book 1:N Borrowing

## Installation and Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure .env File

Edit the `.env` file and change SECRET_KEY:

```env
SECRET_KEY=your-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./library.db
```

### 4. Start Server

```bash
uvicorn app.main:app --reload
```

Server will start at http://127.0.0.1:8000

## API Usage

### API Documentation

After starting the server, available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Example Requests

#### 1. User Registration

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "email": "user1@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "user"
  }'
```

#### 2. Login

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Create Book (admin role required)

```bash
curl -X POST "http://127.0.0.1:8000/books/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "isbn": "978-0-06-112008-4",
    "published_year": 1960,
    "quantity": 5
  }'
```

#### 4. Get List of Books

```bash
curl -X GET "http://127.0.0.1:8000/books/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 5. Search Books

```bash
curl -X GET "http://127.0.0.1:8000/books/?search=Harper" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 6. Borrow a Book

```bash
curl -X POST "http://127.0.0.1:8000/borrowings/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "borrow_date": "2024-02-12"
  }'
```

#### 7. Return a Book

```bash
curl -X PUT "http://127.0.0.1:8000/borrowings/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "return_date": "2024-02-20",
    "status": "returned"
  }'
```

## User Roles

### User
- View list of books
- Search books
- Create borrowings (borrow books)
- View own borrowings
- Return own books

### Admin
- All user capabilities +
- Create/edit/delete books
- Manage users
- View all borrowings
- Delete borrowings

## Creating Administrator

### Option 1: Through Database

1. Register user via API
2. Open `library.db` file with SQLite browser
3. Find user and change `role` field to `'admin'`

### Option 2: Through Python Script

Create file `create_admin.py`:

```python
from app.database import SessionLocal
from app.crud import user as user_crud
from app.schemas.user import UserCreate

db = SessionLocal()

admin_data = UserCreate(
    username="admin",
    email="admin@library.com",
    password="admin123",
    full_name="Administrator",
    role="admin"
)

admin = user_crud.create_user(db, admin_data)
print(f"Created admin: {admin.username}")

db.close()
```

Run:
```bash
python create_admin.py
```

## Testing via Swagger UI

1. Go to http://127.0.0.1:8000/docs
2. Register user via `/auth/register`
3. Login via `/auth/login` - copy token
4. Click "Authorize" button at top
5. Paste token in format: `your_token` (without "Bearer")
6. Test all endpoints through interface

## Implementation Features

### CRUD Operations
Full CRUD implemented for **books** entity:
- Create: `POST /books/`
- Read: `GET /books/` and `GET /books/{id}`
- Update: `PUT /books/{id}`
- Delete: `DELETE /books/{id}`

### Security
- Passwords hashed using bcrypt
- JWT tokens for authentication
- Role-based access control

### Database
- SQLite for data storage
- SQLAlchemy ORM for database operations
- Automatic table creation on startup

### OpenAPI Documentation
- Customized title, description
- Added tags for endpoint grouping
- Detailed descriptions for each endpoint
- Usage examples

## Project Structure

```
library_system/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── users.py         # Users
│   │   │   ├── books.py         # Books (full CRUD)
│   │   │   └── borrowings.py    # Borrowings
│   │   └── deps.py              # Dependencies (auth)
│   ├── core/
│   │   ├── security.py          # JWT, hashing
│   │   └── permissions.py       # Role checking
│   ├── crud/
│   │   ├── user.py              # User CRUD
│   │   ├── book.py              # Book CRUD
│   │   └── borrowing.py         # Borrowing CRUD
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── book.py              # Book model
│   │   └── borrowing.py         # Borrowing model
│   ├── schemas/
│   │   ├── user.py              # Pydantic schemas
│   │   ├── book.py
│   │   ├── borrowing.py
│   │   └── auth.py
│   ├── config.py                # Configuration
│   ├── database.py              # DB setup
│   └── main.py                  # FastAPI application
├── .env                         # Environment variables
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

## Author

FastAPI Laboratory Work
Topic: Library Management System

## License

MIT
