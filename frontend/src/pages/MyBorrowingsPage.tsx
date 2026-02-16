import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { apiService } from '@/services/api';
import type { Borrowing } from '@/types';

const MyBorrowingsPage: React.FC = () => {
  const [borrowings, setBorrowings] = useState<Borrowing[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [returnDialogOpen, setReturnDialogOpen] = useState(false);
  const [selectedBorrowing, setSelectedBorrowing] = useState<Borrowing | null>(null);
  const [returnDate, setReturnDate] = useState(
    new Date().toISOString().split('T')[0]
  );

  const loadBorrowings = async () => {
    try {
      setIsLoading(true);
      const data = await apiService.getMyBorrowings();
      setBorrowings(data);
    } catch (err: any) {
      setError('Не вдалося завантажити бронювання');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadBorrowings();
  }, []);

  const handleReturnClick = (borrowing: Borrowing) => {
    setSelectedBorrowing(borrowing);
    setReturnDialogOpen(true);
  };

  const handleReturnConfirm = async () => {
    if (!selectedBorrowing) return;

    try {
      await apiService.updateBorrowing(selectedBorrowing.id, {
        return_date: returnDate,
        status: 'returned',
      });
      await loadBorrowings();
      setReturnDialogOpen(false);
      setSelectedBorrowing(null);
    } catch (err: any) {
      setError('Не вдалося повернути книгу');
    }
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
      <Typography variant="h4" component="h1" gutterBottom>
        Мої бронювання
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {borrowings.length === 0 ? (
        <Alert severity="info">
          У вас ще немає бронювань. Перейдіть до каталогу, щоб забронювати книгу!
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {borrowings.map((borrowing) => (
            <Grid item xs={12} md={6} key={borrowing.id}>
              <Card>
                <CardContent>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      mb: 2,
                    }}
                  >
                    <Typography variant="h6" component="h2">
                      {borrowing.book_title || 'Невідома книга'}
                    </Typography>
                    <Chip
                      label={
                        borrowing.status === 'borrowed'
                          ? 'Забронована'
                          : 'Повернена'
                      }
                      color={
                        borrowing.status === 'borrowed' ? 'primary' : 'success'
                      }
                      size="small"
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Автор: {borrowing.book_author || 'Невідомо'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    ISBN: {borrowing.book_isbn || 'Невідомо'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Дата бронювання:{' '}
                    {new Date(borrowing.borrow_date).toLocaleDateString('uk-UA')}
                  </Typography>
                  {borrowing.return_date && (
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      gutterBottom
                    >
                      Дата повернення:{' '}
                      {new Date(borrowing.return_date).toLocaleDateString(
                        'uk-UA'
                      )}
                    </Typography>
                  )}

                  {borrowing.status === 'borrowed' && (
                    <Box sx={{ mt: 2 }}>
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => handleReturnClick(borrowing)}
                      >
                        Повернути книгу
                      </Button>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog
        open={returnDialogOpen}
        onClose={() => setReturnDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Повернути книгу</DialogTitle>
        <DialogContent>
          <Typography gutterBottom>
            Ви впевнені, що хочете повернути книгу "
            {selectedBorrowing?.book?.title}"?
          </Typography>
          <TextField
            fullWidth
            label="Дата повернення"
            type="date"
            value={returnDate}
            onChange={(e) => setReturnDate(e.target.value)}
            sx={{ mt: 2 }}
            InputLabelProps={{
              shrink: true,
            }}
            inputProps={{
              max: new Date().toISOString().split('T')[0],
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReturnDialogOpen(false)}>Скасувати</Button>
          <Button onClick={handleReturnConfirm} variant="contained">
            Підтвердити повернення
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MyBorrowingsPage;
