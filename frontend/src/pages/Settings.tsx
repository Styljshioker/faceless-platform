import React from 'react';
import { Container, Paper, TextField, Button, Box, Typography } from '@mui/material';
import { useState } from 'react';

export const Settings: React.FC = () => {
  const [fullName, setFullName] = useState('');
  const [bio, setBio] = useState('');
  const [email, setEmail] = useState('');

  const handleSave = () => {
    // TODO: Save settings
    console.log('Settings saved');
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>⚙️ Settings</Typography>
      <Paper sx={{ p: 4 }}>
        <Box sx={{ display: 'grid', gap: 2 }}>
          <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} fullWidth disabled />
          <TextField label="Full Name" value={fullName} onChange={(e) => setFullName(e.target.value)} fullWidth />
          <TextField label="Bio" value={bio} onChange={(e) => setBio(e.target.value)} fullWidth multiline rows={4} />
          <Button variant="contained" color="primary" onClick={handleSave}>
            Save Settings
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};
