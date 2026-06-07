import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  VideoLibrary,
  Schedule,
  AttachMoney,
  PlayArrow,
  Pause,
} from '@mui/icons-material';
import { MetricCard } from '../components/MetricCard';
import { RecentContent } from '../components/RecentContent';
import { ContentPipeline } from '../components/ContentPipeline';
import { api } from '../services/api';

interface DashboardMetrics {
  totalVideos: number;
  totalViews: number;
  totalRevenue: number;
  activeJobs: number;
  completionRate: number;
  avgProcessingTime: string;
}

export function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const response = await api.get('/analytics/dashboard');
      setMetrics(response.data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box className="flex justify-center items-center h-64">
        <LinearProgress className="w-64" />
      </Box>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Box>
        <Typography variant="h4" className="font-bold text-white mb-2">
          Dashboard
        </Typography>
        <Typography variant="body1" className="text-slate-400">
          Welcome to your Faceless Content Creation Platform
        </Typography>
      </Box>

      {/* Metrics Grid */}
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Total Videos"
            value={metrics?.totalVideos || 0}
            icon={<VideoLibrary />}
            trend="+12%"
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Total Views"
            value={metrics?.totalViews || 0}
            icon={<TrendingUp />}
            trend="+8%"
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Revenue"
            value={`$${metrics?.totalRevenue || 0}`}
            icon={<AttachMoney />}
            trend="+15%"
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Active Jobs"
            value={metrics?.activeJobs || 0}
            icon={<Schedule />}
            trend={metrics?.activeJobs ? 'Processing' : 'Idle'}
            color="info"
          />
        </Grid>
      </Grid>

      {/* Content Pipeline Status */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Card className="bg-slate-800 border border-slate-700">
            <CardContent>
              <Typography variant="h6" className="font-semibold text-white mb-4">
                Content Pipeline Status
              </Typography>
              <ContentPipeline />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} lg={4}>
          <Card className="bg-slate-800 border border-slate-700">
            <CardContent>
              <Typography variant="h6" className="font-semibold text-white mb-4">
                Platform Health
              </Typography>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">AI Voice Service</span>
                  <Chip label="Operational" color="success" size="small" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Content Moderation</span>
                  <Chip label="Operational" color="success" size="small" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Video Processing</span>
                  <Chip label="Operational" color="success" size="small" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Analytics Engine</span>
                  <Chip label="Operational" color="success" size="small" />
                </div>
              </div>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Content */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card className="bg-slate-800 border border-slate-700">
            <CardContent>
              <Typography variant="h6" className="font-semibold text-white mb-4">
                Recent Content
              </Typography>
              <RecentContent />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}
