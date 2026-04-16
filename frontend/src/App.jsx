import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { ChatPage } from './pages/ChatPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { SessionDetailPage } from './pages/SessionDetailPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { DeveloperDashboardPage } from './pages/DeveloperDashboardPage';
import { useAuth } from './hooks/useAuth';

// Role-based dashboard router
const DashboardRouter = () => {
  const { role } = useAuth();
  
  if (role === 'hr_admin' || role === 'superadmin') {
    return <AdminDashboardPage />;
  }
  
  // Default for devs/engineers
  return <DeveloperDashboardPage />;
};

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      
      <Route 
        path="/chat" 
        element={
          <ProtectedRoute>
            <ChatPage />
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <DashboardRouter />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/dashboard/sessions/:sessionId" 
        element={
          <ProtectedRoute requiredRole="hr_admin">
            <SessionDetailPage />
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
};

export default App;
