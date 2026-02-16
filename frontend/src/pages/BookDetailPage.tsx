import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Grid,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { apiService } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import type { Book } from '@/types';

const BookDetailPage: React.FC = () => {
  const { bookId } = useParams<{ bookId: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin } = useAuth();
  const [book, setBook] = useState<Book | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBook();
  }, [bookId]);

  const loadBook = async () => {
    try {
      setIsLoading(true);
      const data = await apiService.getBook(Number(bookId));
      setBook(data);
    } catch (err: any) {
      setError('Не вдалося завантажити книгу');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBorrow = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    navigate(`/borrow/${bookId}`);
  };

  const handleEdit = () => {
    navigate(`/books?edit=${bookId}`);
  };

  const handleDelete = async () => {
    if (!book) return;
    
    if (window.confirm(`Ви впевнені, що хочете видалити книгу "${book.title}"?`)) {
      try {
        await apiService.deleteBook(book.id);
        navigate('/books');
      } catch (err: any) {
        setError('Не вдалося видалити книгу');
      }
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !book) {
    return (
      <Box>
        <Alert severity="error">{error || 'Книгу не знайдено'}</Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/books')}
          sx={{ mt: 2 }}
        >
          Повернутися до каталогу
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/books')}
        sx={{ mb: 3 }}
      >
        Повернутися до каталогу
      </Button>

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h3" component="h1" gutterBottom>
              {book.title}
            </Typography>

            <Typography variant="h5" color="text.secondary" gutterBottom>
              {book.author}
            </Typography>

            <Divider sx={{ my: 3 }} />

            <Grid container spacing={2}>
              {book.isbn && (
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    ISBN
                  </Typography>
                  <Typography variant="body1" fontWeight="medium">
                    {book.isbn}
                  </Typography>
                </Grid>
              )}

              {book.published_year && (
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Рік видання
                  </Typography>
                  <Typography variant="body1" fontWeight="medium">
                    {book.published_year}
                  </Typography>
                </Grid>
              )}

              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Всього примірників
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {book.quantity}
                </Typography>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Доступно для бронювання
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {book.available}
                </Typography>
              </Grid>

              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary">
                  Додано до бібліотеки
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {new Date(book.created_at).toLocaleDateString('uk-UA', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Бокова панель з діями */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Статус книги
              </Typography>

              <Box sx={{ mb: 3 }}>
                <Chip
                  label={book.available > 0 ? 'Доступна' : 'Недоступна'}
                  color={book.available > 0 ? 'success' : 'error'}
                  sx={{ fontSize: '1rem', py: 2, px: 1 }}
                />
              </Box>

              {/* Кнопки для користувачів */}
              {!isAdmin && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    disabled={book.available === 0 || !isAuthenticated}
                    onClick={handleBorrow}
                  >
                    {!isAuthenticated
                      ? 'Увійдіть щоб забронювати'
                      : book.available === 0
                      ? 'Немає в наявності'
                      : 'Забронювати книгу'}
                  </Button>

                  {!isAuthenticated && (
                    <Typography variant="caption" color="text.secondary" textAlign="center">
                      Для бронювання потрібна авторизація
                    </Typography>
                  )}
                </Box>
              )}

              {/* Кнопки для адміністратора */}
              {isAdmin && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Button
                    variant="contained"
                    startIcon={<EditIcon />}
                    fullWidth
                    onClick={handleEdit}
                  >
                    Редагувати
                  </Button>
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<DeleteIcon />}
                    fullWidth
                    onClick={handleDelete}
                  >
                    Видалити книгу
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Про бібліотеку
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Next Read - це онлайн система управління бібліотекою. 
                Бронюйте книги онлайн та забирайте їх у зручний для вас час.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BookDetailPage;