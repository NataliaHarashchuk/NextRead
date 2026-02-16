import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Chip,
} from '@mui/material';
import { apiService } from '@/services/api';
import type { Book } from '@/types';

const BorrowBookPage: React.FC = () => {
  const { bookId } = useParams<{ bookId: string }>();
  const navigate = useNavigate();
  const [book, setBook] = useState<Book | null>(null);
  const [borrowDate, setBorrowDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const loadBook = async () => {
      try {
        setIsLoading(true);
        const data = await apiService.getBook(Number(bookId));
        setBook(data);
      } catch (err: any) {
        setError('Не вдалося завантажити інформацію про книгу');
      } finally {
        setIsLoading(false);
      }
    };

    if (bookId) {
      loadBook();
    }
  }, [bookId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    setSuccess('');

    try {
      await apiService.createBorrowing({
        book_id: Number(bookId),
        borrow_date: borrowDate,
      });
      setSuccess('Книгу успішно забронировано!');
      setTimeout(() => {
        navigate('/my-borrowings');
      }, 2000);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Помилка бронювання. Спробуйте ще раз.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!book) {
    return (
      <Alert severity="error">Книгу не знайдено</Alert>
    );
  }

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto' }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Бронювання книги
        </Typography>

        <Box sx={{ my: 3 }}>
          <Typography variant="h6" gutterBottom>
            {book.title}
          </Typography>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            Автор: {book.author}
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            ISBN: {book.isbn}
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Рік видання: {book.published_year}
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Chip
              label={`Доступно: ${book.available} з ${book.quantity}`}
              color={book.available > 0 ? 'success' : 'error'}
            />
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        {book.available === 0 ? (
          <Alert severity="warning" sx={{ mb: 2 }}>
            На жаль, всі примірники цієї книги зараз забронировані
          </Alert>
        ) : (
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Дата бронювання"
              type="date"
              value={borrowDate}
              onChange={(e) => setBorrowDate(e.target.value)}
              sx={{ mb: 3 }}
              InputLabelProps={{
                shrink: true,
              }}
              inputProps={{
                min: new Date().toISOString().split('T')[0],
              }}
            />

            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/books')}
              >
                Скасувати
              </Button>
              <Button
                fullWidth
                variant="contained"
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Бронювання...' : 'Забронювати'}
              </Button>
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default BorrowBookPage;
