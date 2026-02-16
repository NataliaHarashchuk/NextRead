export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  role: 'admin' | 'user';
  is_active: boolean;
  created_at: string;
}

export interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string | null;
  published_year: number | null;
  quantity: number;
  available: number;
  created_at: string;
}

export interface Borrowing {
  id: number;
  user_id: number;
  book_id: number;
  borrow_date: string;
  return_date: string | null;
  status: 'borrowed' | 'returned';
  created_at: string;
  book?: Book;
  user?: User;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string | null;
  role?: 'user' | 'admin';
}

export interface CreateBookRequest {
  title: string;
  author: string;
  isbn?: string | null;
  published_year?: number | null;
  quantity: number;
}

export interface UpdateBookRequest {
  title?: string;
  author?: string;
  isbn?: string | null;
  published_year?: number | null;
  quantity?: number;
  available?: number;
}

export interface CreateBorrowingRequest {
  book_id: number;
  borrow_date: string;
}

export interface UpdateBorrowingRequest {
  return_date?: string;
  status?: 'borrowed' | 'returned';
}

export interface ApiError {
  detail: string;
}
