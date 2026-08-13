import React, { useState, useEffect } from 'react';
import { AuthContext } from './AuthContextObject';

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => sessionStorage.getItem('token'));
  const [role, setRole] = useState(() => sessionStorage.getItem('role'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      sessionStorage.setItem('token', token);
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUser({
          id: payload.sub,
          role: payload.role,
          email: payload.email,
          departmentRole: payload.department_role,
          onboardingProgress: payload.onboarding_progress
        });
      } catch (e) {
        console.error("Failed to decode JWT", e);
      }
    } else {
      sessionStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  useEffect(() => {
    if (role) {
      sessionStorage.setItem('role', role);
    } else {
      sessionStorage.removeItem('role');
    }
  }, [role]);

  const login = (newToken, newRole) => {
    setToken(newToken);
    setRole(newRole);
  };

  const logout = () => {
    setToken(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, role, user, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};
