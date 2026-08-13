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
      // login auth context
      login(data.access_token, data.role);
      const userRole = (data.role || '').toLowerCase();
      if (userRole === 'admin' || userRole === 'superadmin') {
          navigate('/admin');
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
    <div className="min-h-screen bg-[#F7F5F0] text-stone-900 flex flex-col font-sans selection:bg-blue-100">
      {/* Editorial Grid Pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40"
        style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, #E7E5E4 1px, transparent 0)',
          backgroundSize: '20px 20px'
        }}
      />
      
      <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden z-10">
        <header className="flex items-center justify-between w-full px-6 py-5 lg:px-12 border-b border-stone-200 bg-[#F7F5F0]">
          <div className="flex items-center gap-3">
            <div className="size-7 bg-stone-900 rounded-sm flex items-center justify-center text-stone-100 shadow-sm">
              <span className="font-bold font-mono text-xs tracking-tighter">O.</span>
            </div>
            <h2 className="text-stone-900 text-lg font-serif font-bold tracking-tight">O.N.E.</h2>
          </div>
        </header>

        <main className="flex flex-1 items-center justify-center p-4 sm:p-6 lg:p-8">
          <div className="w-full max-w-[400px]">
            {/* Warm Paper Card */}
            <div className="bg-white border border-stone-200 rounded-md p-8 shadow-sm">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center size-12 rounded-sm bg-[#F2F0EA] mb-4 border border-stone-200 text-stone-900">
                   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"/><path d="M12 3v9h9"/></svg>
                </div>
                <h1 className="text-2xl font-serif font-bold tracking-tight text-stone-900 mb-1">Sign in to Console</h1>
                <p className="text-stone-500 font-mono text-xs uppercase tracking-widest">Onboarding Navigation Environment</p>
              </div>

              <form className="space-y-4" onSubmit={handleSubmit}>
                {error && (
                  <div className="bg-rose-50 text-rose-800 p-3.5 border border-rose-200 rounded-sm text-xs font-mono mb-4">
                    {error}
                  </div>
                )}
                
                <div>
                  <label className="block text-[10px] font-mono font-bold text-stone-500 mb-1.5 uppercase tracking-widest" htmlFor="email">
                    Email address
                  </label>
                  <input 
                    id="email" 
                    type="email" 
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-sm bg-white border border-stone-300 px-3.5 py-2.5 text-stone-900 focus:outline-none focus:border-stone-900 transition-colors placeholder:text-stone-400 text-sm font-medium" 
                    placeholder="name@company.com" 
                  />
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="block text-[10px] font-mono font-bold text-stone-500 uppercase tracking-widest" htmlFor="password">
                      Password
                    </label>
                  </div>
                  <input 
                    id="password" 
                    type="password" 
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full rounded-sm bg-white border border-stone-300 px-3.5 py-2.5 text-stone-900 focus:outline-none focus:border-stone-900 transition-colors placeholder:text-stone-400 text-sm font-medium" 
                    placeholder="••••••••" 
                  />
                </div>
                
                <button 
                  type="submit" 
                  disabled={loading}
                  className="w-full rounded-sm bg-stone-900 py-3 text-xs font-mono font-bold text-white uppercase tracking-widest hover:bg-stone-800 transition-colors mt-6 active:scale-[0.99] disabled:opacity-50 flex justify-center items-center shadow-sm"
                >
                  {loading ? 'AUTHENTICATING...' : 'SIGN IN'}
                </button>
              </form>
            </div>
          </div>
        </main>
        
        <footer className="mt-auto py-8 text-center text-slate-600 text-[10px] font-bold uppercase tracking-[0.2em]">
          © {new Date().getFullYear()} O.N.E Technologies.
        </footer>
      </div>
    </div>
  );
};
