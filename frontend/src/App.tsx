import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from './contexts/AuthContext';
import { Dashboard } from './pages/Dashboard';
import { ContentCreation } from './pages/ContentCreation';
import { Analytics } from './pages/Analytics';
import { Scheduling } from './pages/Scheduling';
import { Monetization } from './pages/Monetization';
import { Settings } from './pages/Settings';
import { Login } from './pages/Login';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { PrivateRoute } from './components/PrivateRoute';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#6366f1',
    },
    secondary: {
      main: '#8b5cf6',
    },
    background: {
      default: '#0f172a',
      paper: '#1e293b',
    },
  },
  typography: {
    fontFamily: 'Inter, system-ui, sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-slate-900">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/*" element={
                <PrivateRoute>
                  <div className="flex">
                    <Sidebar />
                    <div className="flex-1">
                      <Navbar />
                      <main className="p-6">
                        <Routes>
                          <Route path="/" element={<Dashboard />} />
                          <Route path="/content" element={<ContentCreation />} />
                          <Route path="/analytics" element={<Analytics />} />
                          <Route path="/scheduling" element={<Scheduling />} />
                          <Route path="/monetization" element={<Monetization />} />
                          <Route path="/settings" element={<Settings />} />
                        </Routes>
                      </main>
                    </div>
                  </div>
                </PrivateRoute>
              } />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
