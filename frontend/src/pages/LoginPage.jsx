import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { login as apiLogin } from '../api/auth';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await apiLogin(email, password);
      login(data.access_token, data.role);
      
      if (data.role === 'hr_admin' || data.role === 'superadmin') {
        navigate('/dashboard');
      } else {
        navigate('/chat');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F7F5F0] flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <h1 className="text-3xl font-light text-zinc-900 tracking-tight">O.N.E. Identity</h1>
        <p className="mt-2 text-sm text-zinc-500 uppercase tracking-widest font-semibold">Secure Portal Access</p>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-12 px-10 border border-zinc-200 shadow-sm">
          <form className="space-y-8" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 text-red-700 p-4 border border-red-200 text-sm">
                {error}
              </div>
            )}
            
            <div className="space-y-1">
              <label className="block text-xs font-semibold text-zinc-800 uppercase tracking-wider">
                Email Address
              </label>
              <div className="mt-1">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-4 py-3 border border-zinc-300 placeholder-zinc-400 focus:outline-none focus:border-zinc-900 transition-colors sm:text-sm bg-zinc-50"
                  placeholder="name@company.com"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-semibold text-zinc-800 uppercase tracking-wider">
                Password
              </label>
              <div className="mt-1">
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-4 py-3 border border-zinc-300 placeholder-zinc-400 focus:outline-none focus:border-zinc-900 transition-colors sm:text-sm bg-zinc-50"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-4 px-4 border border-transparent text-sm font-medium text-white bg-zinc-900 hover:bg-zinc-800 focus:outline-none focus:border-zinc-900 focus:ring-0 active:bg-zinc-900 disabled:opacity-50 transition-colors uppercase tracking-widest"
              >
                {loading ? 'Authenticating...' : 'Sign In'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
