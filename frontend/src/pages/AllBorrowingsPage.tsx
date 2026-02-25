import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import { apiService } from '@/services/api';
import type { Borrowing } from '@/types';

type BorrowingStatus = 'borrowed' | 'returned';

const AllBorrowingsPage: React.FC = () => {
  const [borrowings, setBorrowings] = useState<Borrowing[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState<BorrowingStatus | 'all'>('all');

  useEffect(() => {
    loadBorrowings();
  }, [statusFilter]);

  const loadBorrowings = async () => {
    try {
      setIsLoading(true);
      setError('');
      const status = statusFilter === 'all' ? undefined : statusFilter;
      const data = await apiService.getAllBorrowings(status);
      setBorrowings(sortBorrowings(data));
    } catch (err: any) {
      setError('Не вдалося завантажити бронювання');
    } finally {
      setIsLoading(false);
    }
  };

  const sortBorrowings = (data: Borrowing[]): Borrowing[] => {
    return [...data].sort((a, b) => {
      if (a.status !== b.status) {
        return a.status === 'borrowed' ? -1 : 1;
      }
      return new Date(b.borrow_date).getTime() - new Date(a.borrow_date).getTime();
    });
  };

  const getStatusColor = (status: string): 'success' | 'info' => {
    return status === 'returned' ? 'success' : 'info';
  };

  const getStatusText = (status: string): string => {
    return status === 'returned' ? 'Повернена' : 'Забронована';
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: BorrowingStatus | 'all') => {
    setStatusFilter(newValue);
  };

  const borrowedCount = borrowings.filter(b => b.status === 'borrowed').length;
  const returnedCount = borrowings.filter(b => b.status === 'returned').length;

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
        Всі бронювання
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Перегляд усіх бронювань користувачів
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Статистика */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Всього бронювань
              </Typography>
              <Typography variant="h4">{borrowings.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Активні
              </Typography>
              <Typography variant="h4" color="info.main">
                {borrowedCount}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Повернені
              </Typography>
              <Typography variant="h4" color="success.main">
                {returnedCount}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={statusFilter}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label={`Всі (${borrowings.length})`} value="all" />
          <Tab label={`Активні (${borrowedCount})`} value="borrowed" />
          <Tab label={`Повернені (${returnedCount})`} value="returned" />
        </Tabs>
      </Paper>

      {borrowings.length === 0 ? (
        <Alert severity="info">Бронювань не знайдено</Alert>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Користувач</TableCell>
                <TableCell>Книга</TableCell>
                <TableCell>Автор</TableCell>
                <TableCell>Дата бронювання</TableCell>
                <TableCell>Дата повернення</TableCell>
                <TableCell>Статус</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {borrowings.map((borrowing) => (
                <TableRow
                  key={borrowing.id}
                  sx={{
                    '&:hover': { backgroundColor: 'action.hover' },
                    backgroundColor:
                      borrowing.status === 'borrowed'
                        ? 'rgba(33, 150, 243, 0.05)'
                        : 'rgba(76, 175, 80, 0.05)',
                  }}
                >
                  <TableCell>{borrowing.id}</TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2" fontWeight="medium">
                        {borrowing.user?.full_name || borrowing.user?.username}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        @{borrowing.user?.username}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="medium">
                      {borrowing.book?.title}
                    </Typography>
                    {borrowing.book?.isbn && (
                      <Typography variant="caption" color="text.secondary">
                        ISBN: {borrowing.book?.isbn}
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell>{borrowing.book?.author}</TableCell>
                  <TableCell>
                    {new Date(borrowing.borrow_date).toLocaleDateString('uk-UA', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </TableCell>
                  <TableCell>
                    {borrowing.return_date ? (
                      new Date(borrowing.return_date).toLocaleDateString('uk-UA', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        —
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={getStatusText(borrowing.status)}
                      color={getStatusColor(borrowing.status)}
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default AllBorrowingsPage;