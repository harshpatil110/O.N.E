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
      
      // Always route to dashboard on successful login
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-slate-300 flex flex-col font-sans selection:bg-[#4c6ef5]/30">
      {/* Background grid pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40 mix-blend-screen"
        style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0)',
          backgroundSize: '24px 24px'
        }}
      />
      
      <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden z-10">
        <header className="flex items-center justify-between w-full px-6 py-5 lg:px-12 border-b border-[#1f1f23] bg-[#0a0a0c]/50 backdrop-blur-md">
          <div className="flex items-center gap-2.5">
            <div className="size-7 bg-[#4c6ef5] rounded flex items-center justify-center text-white shadow-lg shadow-[#4c6ef5]/20">
              <span className="font-bold font-mono text-sm tracking-tighter">O.</span>
            </div>
            <h2 className="text-white text-lg font-extrabold tracking-tight">O.N.E</h2>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a className="text-sm font-medium text-slate-400 hover:text-white transition-colors" href="#">Documentation</a>
            <a className="text-sm font-medium text-slate-400 hover:text-white transition-colors" href="#">System Status</a>
          </div>
        </header>

        <main className="flex flex-1 items-center justify-center p-4 sm:p-6 lg:p-8">
          <div className="w-full max-w-[420px]">
            {/* Dark Card */}
            <div className="bg-[#111114] border border-[#1f1f23] rounded-xl p-8 shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
              <div className="text-center mb-10">
                <div className="inline-flex items-center justify-center size-14 rounded-xl bg-white/5 mb-6 border border-white/10 text-[#4c6ef5]">
                   <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"/><path d="M12 3v9h9"/></svg>
                </div>
                <h1 className="text-2xl font-bold tracking-tight text-white mb-2">Sign in to Console</h1>
                <p className="text-slate-400 text-sm">Onboarding Navigation Environment</p>
              </div>

              <div className="space-y-3">
                <button className="flex w-full items-center justify-center gap-3 rounded-lg h-11 px-5 bg-transparent border border-[#1f1f23] hover:bg-white/5 text-white text-sm font-semibold transition-all shadow-sm">
                  <img alt="" className="w-4 h-4 invert" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD0N2FhrdhdvWe9gTAduartuBxFlX5CuUchWCKuAY2cT8JYz4vQ2SeHk-1IAILy-DojUbpzQhm2PpMMbZ9IPY9PGCz3PFZ9sQt0FTn-640h81lxYrquKcLhWwlODaieXEatEKqXUA65LyG0HnKN-cnr7e8rsU6geUkszo7Qa9dlLbR8jJSun__rdJ31zqUIuka9hTBzfg7tB0hGHwTm5BDqjolRFszXW3Iiv3mgwp12SUIVIS77rGqbnhaSVuOyvabEI5ah-tN8O2rl" />
                  <span>GitHub</span>
                </button>
                <button className="flex w-full items-center justify-center gap-3 rounded-lg h-11 px-5 bg-transparent border border-[#1f1f23] hover:bg-white/5 text-white text-sm font-semibold transition-all shadow-sm">
                  <img alt="" className="w-4 h-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD44uybZgB-OQB91Ilm5rA6lVZ2Kcqv2XvMy5CNhj3e0vk7M9cWsptEAascgCVv28mJzoVqXBJVCDkD-Ol9hW4CJQyoXyY4-CmX0FCy49Fw3xChPmxvNoVZ9SmU56Pmjc3RhwQKi-w2wYyiVaZ1JuoRuUb0c6IJo3YWLGI5DESsrc2hAXvc9S_H1nZvtQ1XNNRxfNgUrMzYgSW6E4Q9AsP3aLMJLQVUi8l2r1bUCBGyqwId6gMumoH_gYorm00iWnCig8XqVTnKvEMa" />
                  <span>Google</span>
                </button>
              </div>

              <div className="relative my-8">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-[#1f1f23]"></div>
                </div>
                <div className="relative flex justify-center text-[10px] font-bold uppercase tracking-widest">
                  <span className="bg-[#111114] px-3 text-slate-500">OR</span>
                </div>
              </div>

              <form className="space-y-4" onSubmit={handleSubmit}>
                {error && (
                  <div className="bg-red-500/10 text-red-400 p-4 border border-red-500/20 rounded-lg text-sm mb-4">
                    {error}
                  </div>
                )}
                
                <div>
                  <label className="block text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider" htmlFor="email">
                    Email address
                  </label>
                  <input 
                    id="email" 
                    type="email" 
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-lg bg-[#0a0a0c]/50 border border-[#1f1f23] px-4 py-2.5 text-white focus:outline-none focus:ring-1 focus:ring-[#4c6ef5] focus:border-[#4c6ef5] transition-all placeholder:text-slate-600 text-sm" 
                    placeholder="name@company.com" 
                  />
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider" htmlFor="password">
                      Password
                    </label>
                    <a className="text-xs text-[#4c6ef5] font-semibold hover:text-[#4c6ef5]/80 transition-colors" href="#">
                      Forgot password?
                    </a>
                  </div>
                  <input 
                    id="password" 
                    type="password" 
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full rounded-lg bg-[#0a0a0c]/50 border border-[#1f1f23] px-4 py-2.5 text-white focus:outline-none focus:ring-1 focus:ring-[#4c6ef5] focus:border-[#4c6ef5] transition-all placeholder:text-slate-600 text-sm" 
                    placeholder="••••••••" 
                  />
                </div>
                
                <button 
                  type="submit" 
                  disabled={loading}
                  className="w-full rounded-lg bg-[#4c6ef5] py-3 text-sm font-bold text-white shadow-lg shadow-[#4c6ef5]/25 hover:bg-[#4c6ef5]/90 transition-all mt-6 active:scale-[0.98] disabled:opacity-50 flex justify-center items-center"
                >
                  {loading ? 'AUTHENTICATING...' : 'SIGN IN'}
                </button>
              </form>
              
              <div className="mt-8 text-center pt-6 border-t border-[#1f1f23]">
                <p className="text-sm font-medium text-slate-400">
                  New here? <a className="text-[#4c6ef5] font-bold hover:underline" href="#">Create an account</a>
                </p>
              </div>
            </div>

            <div className="mt-10 flex justify-center gap-8 text-xs text-slate-500 font-semibold uppercase tracking-wider">
              <a className="hover:text-white transition-colors" href="#">Privacy</a>
              <a className="hover:text-white transition-colors" href="#">Terms</a>
              <a className="hover:text-white transition-colors" href="#">Help</a>
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
