import React, { useEffect, useState } from 'react';
import { Container, Paper, Button, Box, Typography, Card, CardContent, List, ListItem, ListItemText } from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface ScheduledContent {
  id: string;
  title: string;
  scheduled_publish: string;
  status: string;
}

export const Scheduling: React.FC = () => {
  const [scheduled, setScheduled] = useState<ScheduledContent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchScheduled = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${API_URL}/api/v1/scheduling/scheduled`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setScheduled(response.data);
      } catch (error) {
        console.error('Failed to fetch scheduled content:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchScheduled();
  }, []);

  if (loading) return <Typography>Loading...</Typography>;

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>⏰ Scheduling</Typography>
      <Card>
        <CardContent>
          {scheduled.length === 0 ? (
            <Typography>No scheduled content</Typography>
          ) : (
            <List>
              {scheduled.map((item) => (
                <ListItem key={item.id} divider>
                  <ListItemText
                    primary={item.title}
                    secondary={`Scheduled: ${new Date(item.scheduled_publish).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};
