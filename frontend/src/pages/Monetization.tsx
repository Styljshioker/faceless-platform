import React, { useEffect, useState } from 'react';
import { Container, Paper, Card, CardContent, Box, Typography, Button } from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface MonetizationData {
  total_earnings: number;
  pending_payout: number;
  paid_out: number;
  subscription_plan: string;
}

export const Monetization: React.FC = () => {
  const [data, setData] = useState<MonetizationData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMonetization = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${API_URL}/api/v1/monetization/earnings`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setData(response.data);
      } catch (error) {
        console.error('Failed to fetch monetization:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMonetization();
  }, []);

  if (loading) return <Typography>Loading...</Typography>;

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>💰 Monetization</Typography>
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 2 }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Earnings
            </Typography>
            <Typography variant="h5">${(data?.total_earnings || 0).toFixed(2)}</Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Pending Payout
            </Typography>
            <Typography variant="h5">${(data?.pending_payout || 0).toFixed(2)}</Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Already Paid Out
            </Typography>
            <Typography variant="h5">${(data?.paid_out || 0).toFixed(2)}</Typography>
          </CardContent>
        </Card>
      </Box>
      <Box sx={{ mt: 4 }}>
        <Button variant="contained" color="primary" size="large">
          Request Payout
        </Button>
      </Box>
    </Container>
  );
};
