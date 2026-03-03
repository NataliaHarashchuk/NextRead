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
  Divider,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import LocalOfferIcon from '@mui/icons-material/LocalOffer';
import { apiService } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import type { Book } from '@/types';
import BookForm from '@/components/books/BookForm';

const BooksPage: React.FC = () => {
  const { isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();

  const [books, setBooks] = useState<Book[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [allTags, setAllTags] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const [openDialog, setOpenDialog] = useState(false);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [bookToDelete, setBookToDelete] = useState<Book | null>(null);
  const [loginDialogOpen, setLoginDialogOpen] = useState(false);

  // ── load tags once ────────────────────────────────────────────────────────
  useEffect(() => {
    apiService.getAllTags().then(setAllTags).catch(() => {});
  }, []);

  // ── load books (debounced on text, immediate on tag change) ───────────────
  const loadBooks = async (query: string, tags: string[]) => {
    try {
      setIsLoading(true);
      setError('');
      const data = await apiService.getBooks(query || undefined, tags.length ? tags : undefined);
      setBooks(data);
    } catch {
      setError('Не вдалося завантажити книги з сервера');
    } finally {
      setIsLoading(false);
    }
  };

  // debounce text search
  useEffect(() => {
    const t = setTimeout(() => loadBooks(searchQuery, selectedTags), 400);
    return () => clearTimeout(t);
  }, [searchQuery]);

  // immediate on tag change
  useEffect(() => {
    loadBooks(searchQuery, selectedTags);
  }, [selectedTags]);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag],
    );
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedTags([]);
  };

  // ── handlers ──────────────────────────────────────────────────────────────
  const handleBorrow = (bookId: string) => {
    if (!isAuthenticated) { setLoginDialogOpen(true); return; }
    navigate(`/borrow/${bookId}`);
  };

  const handleAddBook = () => { setSelectedBook(null); setOpenDialog(true); };
  const handleEditBook = (book: Book) => { setSelectedBook(book); setOpenDialog(true); };

  const handleDeleteClick = (book: Book) => { setBookToDelete(book); setDeleteConfirmOpen(true); };
  const handleDeleteConfirm = async () => {
    if (!bookToDelete) return;
    try {
      await apiService.deleteBook(bookToDelete.id);
      // refresh tags too (a tag might have been removed with the book)
      apiService.getAllTags().then(setAllTags).catch(() => {});
      await loadBooks(searchQuery, selectedTags);
      setDeleteConfirmOpen(false);
      setBookToDelete(null);
    } catch {
      setError('Не вдалося видалити книгу');
    }
  };

  const handleDialogClose = () => { setOpenDialog(false); setSelectedBook(null); };
  const handleBookSaved = () => {
    // refresh tags in case new ones were added
    apiService.getAllTags().then(setAllTags).catch(() => {});
    loadBooks(searchQuery, selectedTags);
    handleDialogClose();
  };

  const hasFilters = searchQuery.length > 0 || selectedTags.length > 0;

  return (
    <Box>
      {/* ── header ── */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="h4" component="h1">Каталог книг</Typography>
        {isAdmin && (
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleAddBook}>
            Додати книгу
          </Button>
        )}
      </Box>

      {/* ── search ── */}
      <TextField
        fullWidth
        placeholder="Пошук за назвою або автором…"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        sx={{ mb: 2 }}
        InputProps={{
          startAdornment: <InputAdornment position="start"><SearchIcon /></InputAdornment>,
          endAdornment: isLoading && <InputAdornment position="end"><CircularProgress size={20} /></InputAdornment>,
        }}
      />

      {/* ── tag filter panel ── */}
      {allTags.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <LocalOfferIcon fontSize="small" color="action" />
            <Typography variant="body2" color="text.secondary">Фільтр за тегами:</Typography>
            {hasFilters && (
              <Button size="small" variant="text" onClick={clearFilters} sx={{ ml: 'auto', fontSize: '0.75rem' }}>
                Скинути фільтри
              </Button>
            )}
          </Box>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.75 }}>
            {allTags.map((tag) => (
              <Chip
                key={tag}
                label={tag}
                size="small"
                clickable
                onClick={() => toggleTag(tag)}
                color={selectedTags.includes(tag) ? 'primary' : 'default'}
                variant={selectedTags.includes(tag) ? 'filled' : 'outlined'}
              />
            ))}
          </Box>
          {selectedTags.length > 0 && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
              Активні теги: {selectedTags.join(', ')}
            </Typography>
          )}
          <Divider sx={{ mt: 2 }} />
        </Box>
      )}

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {/* ── book grid ── */}
      {!isLoading && books.length === 0 ? (
        <Alert severity="info">
          {hasFilters ? 'За вашим запитом нічого не знайдено.' : 'Каталог порожній'}
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {books.map((book) => (
            <Grid item xs={12} sm={6} md={4} key={book.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'all 0.2s',
                  cursor: 'pointer',
                  '&:hover': { transform: 'translateY(-4px)', boxShadow: 6, '& .book-title': { color: 'primary.main' } },
                }}
                onClick={() => navigate(`/books/${book.id}`)}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="h2" gutterBottom className="book-title">
                    {book.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Автор: {book.author}
                  </Typography>
                  {book.isbn && (
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      ISBN: {book.isbn}
                    </Typography>
                  )}
                  {book.published_year && (
                    <Typography variant="body2" color="text.secondary">
                      Рік: {book.published_year}
                    </Typography>
                  )}

                  {/* tags */}
                  {book.tags && book.tags.length > 0 && (
                    <Box sx={{ mt: 1.5, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {book.tags.map((tag) => (
                        <Chip
                          key={tag}
                          label={tag}
                          size="small"
                          variant="outlined"
                          color="secondary"
                          clickable
                          onClick={(e) => { e.stopPropagation(); toggleTag(tag); }}
                          sx={{ fontSize: '0.7rem', height: 20 }}
                        />
                      ))}
                    </Box>
                  )}

                  <Box sx={{ mt: 1.5, display: 'flex', gap: 1 }}>
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
                    onClick={(e) => { e.stopPropagation(); handleBorrow(book.id); }}
                  >
                    Забронювати
                  </Button>
                  {isAdmin && (
                    <Box>
                      <Button size="small" startIcon={<EditIcon />} onClick={(e) => { e.stopPropagation(); handleEditBook(book); }}>
                        Змінити
                      </Button>
                      <Button size="small" color="error" startIcon={<DeleteIcon />} onClick={(e) => { e.stopPropagation(); handleDeleteClick(book); }}>
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
        <DialogTitle>{selectedBook ? 'Редагувати книгу' : 'Додати нову книгу'}</DialogTitle>
        <DialogContent>
          <BookForm book={selectedBook} onSave={handleBookSaved} onCancel={handleDialogClose} />
        </DialogContent>
      </Dialog>

      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Підтвердження видалення</DialogTitle>
        <DialogContent>
          <Typography>Ви впевнені, що хочете видалити книгу "{bookToDelete?.title}"?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Скасувати</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">Видалити</Button>
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
          <Button onClick={() => navigate('/register')} variant="outlined">Реєстрація</Button>
          <Button onClick={() => { setLoginDialogOpen(false); navigate('/login'); }} variant="contained" autoFocus>Увійти</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BooksPage;