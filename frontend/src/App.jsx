import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { ChatPage } from './pages/ChatPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { AdminDevelopersPage } from './pages/AdminDevelopersPage';
import { AdminAnalyticsPage } from './pages/AdminAnalyticsPage';
import TaskVerification from './pages/TaskVerification';
import { AdminSettingsPage } from './pages/AdminSettingsPage';
import { SessionDetailPage } from './pages/SessionDetailPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { DeveloperDashboardPage } from './pages/DeveloperDashboardPage';
import { KnowledgeBasePage } from './pages/KnowledgeBasePage';
import { ChecklistPage } from './pages/ChecklistPage';
import { DashboardLayout } from './layouts/DashboardLayout';
import { AdminLayout } from './components/AdminLayout';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      
      <Route element={<DashboardLayout />}>
        <Route 
          path="/chat" 
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/checklist" 
          element={
            <ProtectedRoute>
              <ChecklistPage />
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
      </Route>
      
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
            <AdminLayout />
          </ProtectedRoute>
        } 
      >
        <Route index element={<AdminDashboardPage />} />
        <Route path="developers" element={<AdminDevelopersPage />} />
        <Route path="verification" element={<TaskVerification />} />
        <Route path="analytics" element={<AdminAnalyticsPage />} />
        <Route path="settings" element={<AdminSettingsPage />} />
        <Route path="sessions/:sessionId" element={<SessionDetailPage />} />
      </Route>
    </Routes>
  );
};

export default App;
