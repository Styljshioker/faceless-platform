import React, { useState } from 'react';
import { Container, Paper, TextField, Button, Box, Typography, Select, MenuItem, FormControl, InputLabel, Alert } from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TEMPLATES = [
  { id: 'template-1', name: 'Modern Tech' },
  { id: 'template-2', name: 'Business' },
  { id: 'template-3', name: 'Educational' },
  { id: 'template-4', name: 'Entertainment' },
];

const VOICES = [
  { id: 'professional-male', name: 'Professional Male' },
  { id: 'professional-female', name: 'Professional Female' },
  { id: 'british-male', name: 'British Male' },
  { id: 'british-female', name: 'British Female' },
];

export const ContentCreation: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [script, setScript] = useState('');
  const [templateId, setTemplateId] = useState('template-1');
  const [voiceId, setVoiceId] = useState('professional-male');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('access_token');
      await axios.post(
        `${API_URL}/api/v1/content/`,
        { title, description, script, template_id: templateId, voice_id: voiceId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Content created successfully!');
      setTitle('');
      setDescription('');
      setScript('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create content');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>🎨 Create Content</Typography>
      <Paper sx={{ p: 4 }}>
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            margin="normal"
            multiline
            rows={3}
          />
          <TextField
            fullWidth
            label="Script"
            value={script}
            onChange={(e) => setScript(e.target.value)}
            margin="normal"
            multiline
            rows={6}
            required
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Template</InputLabel>
            <Select value={templateId} onChange={(e) => setTemplateId(e.target.value)}>
              {TEMPLATES.map((t) => (
                <MenuItem key={t.id} value={t.id}>
                  {t.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth margin="normal">
            <InputLabel>Voice</InputLabel>
            <Select value={voiceId} onChange={(e) => setVoiceId(e.target.value)}>
              {VOICES.map((v) => (
                <MenuItem key={v.id} value={v.id}>
                  {v.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            fullWidth
            variant="contained"
            color="primary"
            type="submit"
            sx={{ mt: 3 }}
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Content'}
          </Button>
        </form>
      </Paper>
    </Container>
  );
};
