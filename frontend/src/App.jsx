import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { ChatPage } from './pages/ChatPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { AdminDevelopersPage } from './pages/AdminDevelopersPage';
import { AdminAnalyticsPage } from './pages/AdminAnalyticsPage';
import { AdminSettingsPage } from './pages/AdminSettingsPage';
import { SessionDetailPage } from './pages/SessionDetailPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { DeveloperDashboardPage } from './pages/DeveloperDashboardPage';
import { KnowledgeBasePage } from './pages/KnowledgeBasePage';
import { useAuth } from './hooks/useAuth';

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
            <DeveloperDashboardPage />
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/admin" 
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminDashboardPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/docs" 
        element={
          <ProtectedRoute>
            <KnowledgeBasePage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/admin/developers" 
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminDevelopersPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/admin/analytics" 
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminAnalyticsPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/admin/settings" 
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminSettingsPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/admin/sessions/:sessionId" 
        element={
          <ProtectedRoute requiredRole="admin">
            <SessionDetailPage />
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
};

export default App;
