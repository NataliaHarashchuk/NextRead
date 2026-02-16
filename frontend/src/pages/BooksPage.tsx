import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  TextField,
  InputAdornment,
  Alert,
  CircularProgress,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { apiService } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import type { Book } from '@/types';
import BookForm from '@/components/books/BookForm';

const BooksPage: React.FC = () => {
  const { isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [books, setBooks] = useState<Book[]>([]);
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [bookToDelete, setBookToDelete] = useState<Book | null>(null);

  const loadBooks = async () => {
    try {
      setIsLoading(true);
      const data = await apiService.getBooks();
      setBooks(data);
      setFilteredBooks(data);
    } catch (err: any) {
      setError('Не вдалося завантажити книги');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, []);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredBooks(books);
    } else {
      const query = searchQuery.toLowerCase();
      const filtered = books.filter(
        (book) =>
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.isbn?.toLowerCase().includes(query)
      );
      setFilteredBooks(filtered);
    }
  }, [searchQuery, books]);

  const [loginDialogOpen, setLoginDialogOpen] = useState(false);

  const handleBorrow = (bookId: number) => {
    if (!isAuthenticated) {
      setLoginDialogOpen(true);
      return;
    }
    navigate(`/borrow/${bookId}`);
  };

  const handleLoginRedirect = () => {
    setLoginDialogOpen(false);
    navigate('/login');
  };

  const handleAddBook = () => {
    setSelectedBook(null);
    setOpenDialog(true);
  };

  const handleEditBook = (book: Book) => {
    setSelectedBook(book);
    setOpenDialog(true);
  };

  const handleDeleteClick = (book: Book) => {
    setBookToDelete(book);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!bookToDelete) return;

    try {
      await apiService.deleteBook(bookToDelete.id);
      await loadBooks();
      setDeleteConfirmOpen(false);
      setBookToDelete(null);
    } catch (err: any) {
      setError('Не вдалося видалити книгу');
    }
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
    setSelectedBook(null);
  };

  const handleBookSaved = () => {
    loadBooks();
    handleDialogClose();
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
          flexWrap: 'wrap',
          gap: 2,
        }}
      >
        <Typography variant="h4" component="h1">
          Каталог книг
        </Typography>
        {isAdmin && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddBook}
          >
            Додати книгу
          </Button>
        )}
      </Box>

      <TextField
        fullWidth
        placeholder="Пошук за назвою, автором або ISBN..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        sx={{ mb: 3 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {filteredBooks.length === 0 ? (
        <Alert severity="info">
          {searchQuery
            ? 'Книги не знайдено. Спробуйте інший запит.'
            : 'Каталог порожній'}
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {filteredBooks.map((book) => (
            <Grid item xs={12} sm={6} md={4} key={book.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'all 0.2s',
                  cursor: 'pointer',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 6,
                    '& .book-title': {
                      color: 'primary.main',
                    },
                  },
                }}
                onClick={() => navigate(`/books/${book.id}`)}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6"
                    component="h2"
                    gutterBottom
                    className="book-title"
                    sx={{ transition: 'color 0.2s' }}
                  >
                    {book.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Автор: {book.author}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    ISBN: {book.isbn}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Рік видання: {book.published_year}
                  </Typography>
                  <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip
                      label={`Всього: ${book.quantity}`}
                      size="small"
                      color="default"
                    />
                    <Chip
                      label={`Доступно: ${book.available}`}
                      size="small"
                      color={book.available > 0 ? 'success' : 'error'}
                    />
                  </Box>
                </CardContent>
                <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
                  <Button
                    size="small"
                    variant="contained"
                    disabled={book.available === 0}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleBorrow(book.id);
                    }}
                  >
                    {book.available === 0 ? 'Немає в наявності' : 'Забронювати'}
                  </Button>
                  {isAdmin && (
                    <Box>
                      <Button
                        size="small"
                        startIcon={<EditIcon />}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditBook(book);
                        }}
                      >
                        Змінити
                      </Button>
                      <Button
                        size="small"
                        color="error"
                        startIcon={<DeleteIcon />}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteClick(book);
                        }}
                      >
                        Видалити
                      </Button>
                    </Box>
                  )}
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={openDialog} onClose={handleDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedBook ? 'Редагувати книгу' : 'Додати нову книгу'}
        </DialogTitle>
        <DialogContent>
          <BookForm book={selectedBook} onSave={handleBookSaved} onCancel={handleDialogClose} />
        </DialogContent>
      </Dialog>

      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Підтвердження видалення</DialogTitle>
        <DialogContent>
          <Typography>
            Ви впевнені, що хочете видалити книгу "{bookToDelete?.title}"?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Скасувати</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Видалити
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={loginDialogOpen} onClose={() => setLoginDialogOpen(false)}>
        <DialogTitle>Потрібна авторизація</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Щоб забронювати книгу, будь ласка, увійдіть у свій обліковий запис або зареєструйтеся.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setLoginDialogOpen(false)}>Скасувати</Button>
          <Button onClick={() => navigate('/register')} variant="outlined">
            Реєстрація
          </Button>
          <Button onClick={handleLoginRedirect} variant="contained" autoFocus>
            Увійти
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BooksPage;
