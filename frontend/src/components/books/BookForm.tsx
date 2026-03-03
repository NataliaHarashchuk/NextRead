import React, { useState, useEffect, KeyboardEvent } from 'react';
import {
  Box,
  TextField,
  Button,
  Alert,
  Chip,
  Typography,
  InputAdornment,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
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
    tags: [],
  });
  const [tagInput, setTagInput] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (book) {
      setFormData({
        title: book.title,
        author: book.author,
        isbn: book.isbn ?? '',
        published_year: book.published_year ?? new Date().getFullYear(),
        quantity: book.quantity,
        tags: book.tags ?? [],
      });
    } else {
      // reset form when opening for new book
      setFormData({
        title: '',
        author: '',
        isbn: '',
        published_year: new Date().getFullYear(),
        quantity: 1,
        tags: [],
      });
    }
    setTagInput('');
    setError('');
  }, [book]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'published_year' || name === 'quantity' ? Number(value) : value,
    });
    setError('');
  };

  // ── tag helpers ─────────────────────────────────────────────────────────
  const addTag = () => {
    const tag = tagInput.trim().toLowerCase();
    if (!tag) return;
    if ((formData.tags ?? []).includes(tag)) { setTagInput(''); return; }
    setFormData((prev) => ({ ...prev, tags: [...(prev.tags ?? []), tag] }));
    setTagInput('');
  };

  const removeTag = (tag: string) => {
    setFormData((prev) => ({ ...prev, tags: (prev.tags ?? []).filter((t) => t !== tag) }));
  };

  const handleTagKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); addTag(); }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // ── normalize: empty string → null so MongoDB unique index isn't triggered
    const payload: CreateBookRequest = {
      ...formData,
      isbn: formData.isbn?.trim() || null,
      published_year: formData.published_year || null,
    };

    try {
      if (book) {
        await apiService.updateBook(book.id, payload);
      } else {
        await apiService.createBook(payload);
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
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TextField
        margin="normal" required fullWidth
        name="title" label="Назва книги"
        value={formData.title} onChange={handleChange}
      />
      <TextField
        margin="normal" required fullWidth
        name="author" label="Автор"
        value={formData.author} onChange={handleChange}
      />
      <TextField
        margin="normal" fullWidth
        name="isbn" label="ISBN (необов'язково)"
        value={formData.isbn ?? ''}
        onChange={handleChange}
        helperText="Залиште порожнім, якщо ISBN невідомий"
      />
      <TextField
        margin="normal" fullWidth
        name="published_year" label="Рік видання" type="number"
        value={formData.published_year ?? ''}
        onChange={handleChange}
      />
      <TextField
        margin="normal" required fullWidth
        name="quantity" label="Кількість примірників" type="number"
        value={formData.quantity} onChange={handleChange}
        inputProps={{ min: 1 }}
      />

      {/* ── TAGS ── */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
          Теги
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.75, mb: 1 }}>
          {(formData.tags ?? []).map((tag) => (
            <Chip
              key={tag} label={tag} size="small"
              onDelete={() => removeTag(tag)}
              color="primary" variant="outlined"
            />
          ))}
        </Box>
        <TextField
          fullWidth size="small"
          placeholder="Додати тег і натиснути Enter або ,"
          value={tagInput}
          onChange={(e) => setTagInput(e.target.value)}
          onKeyDown={handleTagKeyDown}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <Button size="small" onClick={addTag} sx={{ minWidth: 0, p: '2px 8px' }}>
                  <AddIcon fontSize="small" />
                </Button>
              </InputAdornment>
            ),
          }}
        />
        <Typography variant="caption" color="text.secondary">
          Натисніть Enter або «,» щоб додати тег
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
        <Button onClick={onCancel} fullWidth variant="outlined">Скасувати</Button>
        <Button type="submit" fullWidth variant="contained" disabled={isLoading}>
          {isLoading ? 'Збереження...' : 'Зберегти'}
        </Button>
      </Box>
    </Box>
  );
};

export default BookForm;