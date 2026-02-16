import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Alert } from '@mui/material';
import { apiService } from '@/services/api';
import type { Book, CreateBookRequest } from '@/types';

interface BookFormProps {
  book: Book | null;
  onSave: () => void;
  onCancel: () => void;
}

const BookForm: React.FC<BookFormProps> = ({ book, onSave, onCancel }) => {
  const [formData, setFormData] = useState<CreateBookRequest>({
    title: '',
    author: '',
    isbn: '',
    published_year: new Date().getFullYear(),
    quantity: 1,
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (book) {
      setFormData({
        title: book.title,
        author: book.author,
        isbn: book.isbn,
        published_year: book.published_year,
        quantity: book.quantity,
      });
    }
  }, [book]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'published_year' || name === 'quantity' ? Number(value) : value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (book) {
        await apiService.updateBook(book.id, formData);
      } else {
        await apiService.createBook(formData);
      }
      onSave();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Помилка збереження книги');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TextField
        margin="normal"
        required
        fullWidth
        name="title"
        label="Назва книги"
        value={formData.title}
        onChange={handleChange}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="author"
        label="Автор"
        value={formData.author}
        onChange={handleChange}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="isbn"
        label="ISBN"
        value={formData.isbn}
        onChange={handleChange}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="published_year"
        label="Рік видання"
        type="number"
        value={formData.published_year}
        onChange={handleChange}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="quantity"
        label="Кількість примірників"
        type="number"
        value={formData.quantity}
        onChange={handleChange}
        inputProps={{ min: 1 }}
      />

      <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
        <Button onClick={onCancel} fullWidth variant="outlined">
          Скасувати
        </Button>
        <Button type="submit" fullWidth variant="contained" disabled={isLoading}>
          {isLoading ? 'Збереження...' : 'Зберегти'}
        </Button>
      </Box>
    </Box>
  );
};

export default BookForm;
