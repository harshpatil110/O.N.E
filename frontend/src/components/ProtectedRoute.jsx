import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, role } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Allow superadmin to bypass role checks, or explicitly check for requiredRole
  if (requiredRole && role !== requiredRole && role !== 'superadmin') {
    return <Navigate to="/chat" replace />;
  }

  return children;
};
