import { createBrowserRouter } from 'react-router-dom';
import Layout from '@/components/layout/Layout';
import ProtectedRoute from '@/components/layout/ProtectedRoute';
import HomePage from '@/pages/HomePage';
import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import BooksPage from '@/pages/BooksPage';
import BorrowBookPage from '@/pages/BorrowBookPage';
import MyBorrowingsPage from '@/pages/MyBorrowingsPage';
import BookDetailPage from '@/pages/BookDetailPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'register',
        element: <RegisterPage />,
      },
      {
        path: 'books',
        element: <BooksPage />,
      },
      {
        path: 'books/:bookId',
        element: <BookDetailPage />,
      },
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: 'borrow/:bookId',
            element: <BorrowBookPage />,
          },
          {
            path: 'my-borrowings',
            element: <MyBorrowingsPage />,
          },
        ],
      },
    ],
  },
]);
