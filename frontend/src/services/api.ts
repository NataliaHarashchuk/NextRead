import axios, { AxiosError, AxiosInstance } from 'axios';
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  User,
  Book,
  CreateBookRequest,
  UpdateBookRequest,
  Borrowing,
  CreateBorrowingRequest,
  UpdateBorrowingRequest,
  ApiError,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        if (error.response?.status === 401) {
          const currentPath = window.location.pathname;
          localStorage.removeItem('access_token');
          if (currentPath !== '/login' && currentPath !== '/register') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // AUTH
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await this.api.post<LoginResponse>('/auth/login', data);
    return response.data;
  }

  async register(data: RegisterRequest): Promise<User> {
    const response = await this.api.post<User>('/auth/register', data);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/users/me');
    return response.data;
  }

  // BOOKS
  async getBooks(search?: string): Promise<Book[]> {
    const params = search ? { search } : {};
    const response = await this.api.get<Book[]>('/books/', { params });
    return response.data;
  }

  async getBook(id: number): Promise<Book> {
    const response = await this.api.get<Book>(`/books/${id}`);
    return response.data;
  }

  async createBook(data: CreateBookRequest): Promise<Book> {
    const response = await this.api.post<Book>('/books/', data);
    return response.data;
  }

  async updateBook(id: number, data: UpdateBookRequest): Promise<Book> {
    const response = await this.api.put<Book>(`/books/${id}`, data);
    return response.data;
  }

  async deleteBook(id: number): Promise<void> {
    await this.api.delete(`/books/${id}`);
  }

  // BORROWINGS
  async getBorrowings(): Promise<Borrowing[]> {
    const response = await this.api.get<Borrowing[]>('/borrowings/');
    return response.data;
  }

  async getMyBorrowings(): Promise<Borrowing[]> {
    const response = await this.api.get<Borrowing[]>('/borrowings/my');
    return response.data;
  }

  async createBorrowing(data: CreateBorrowingRequest): Promise<Borrowing> {
    const response = await this.api.post<Borrowing>('/borrowings/', data);
    return response.data;
  }

  async updateBorrowing(
    id: number,
    data: UpdateBorrowingRequest
  ): Promise<Borrowing> {
    const response = await this.api.put<Borrowing>(`/borrowings/${id}`, data);
    return response.data;
  }

  async deleteBorrowing(id: number): Promise<void> {
    await this.api.delete(`/borrowings/${id}`);
  }
}

export const apiService = new ApiService();
