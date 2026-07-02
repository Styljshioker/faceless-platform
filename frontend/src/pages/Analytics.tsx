import React, { useEffect, useState } from 'react';
import { Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, Box, Typography } from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface AnalyticsData {
  id: string;
  views: number;
  likes: number;
  shares: number;
  comments: number;
  engagement_rate: number;
  revenue: number;
}

export const Analytics: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${API_URL}/api/v1/analytics/`, {
          headers: { Authorization: `Bearer ${token}` },
          params: { days: 30, limit: 100 },
        });
        setAnalytics(response.data);
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) return <Typography>Loading...</Typography>;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>📈 Analytics</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell>Views</TableCell>
              <TableCell>Likes</TableCell>
              <TableCell>Shares</TableCell>
              <TableCell>Comments</TableCell>
              <TableCell>Engagement %</TableCell>
              <TableCell>Revenue</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {analytics.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.views.toLocaleString()}</TableCell>
                <TableCell>{item.likes.toLocaleString()}</TableCell>
                <TableCell>{item.shares.toLocaleString()}</TableCell>
                <TableCell>{item.comments.toLocaleString()}</TableCell>
                <TableCell>{item.engagement_rate.toFixed(2)}%</TableCell>
                <TableCell>${item.revenue.toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};
