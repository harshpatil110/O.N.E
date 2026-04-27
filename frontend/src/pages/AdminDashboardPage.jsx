import React, { useEffect, useState } from 'react';
import { getAdminMetrics, getAdminSessions } from '../api/adminApi';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { 
  Search, Bell, Plus, AlertTriangle, ArrowRight,
  LayoutDashboard, Users, BarChart2, MessageSquare, Settings,
  Activity, MoreHorizontal, User as UserIcon, Clock
} from 'lucide-react';

export const AdminDashboardPage = () => {
  const [metrics, setMetrics] = useState(null);
  const [sessionsData, setSessionsData] = useState({ items: [], total: 0 });
  const [loadingMetrics, setLoadingMetrics] = useState(true);
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [error, setError] = useState(null);
  const [adminProfile, setAdminProfile] = useState(null);

  useEffect(() => {
      const fetchAdminProfile = async () => {
          try {
              const token = localStorage.getItem('token');
              const res = await axios.get('http://localhost:8000/api/v1/admin/profile', {
                  headers: { Authorization: `Bearer ${token}` },
                  withCredentials: true,
              });
              setAdminProfile(res.data);
          } catch (err) {
              console.error('Failed to load admin profile', err);
          }
      };
      fetchAdminProfile();
  }, []);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getAdminMetrics();
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load metrics', err);
        setError('Failed to load metrics.');
      } finally {
        setLoadingMetrics(false);
      }
    };
    fetchMetrics();
  }, []);

  useEffect(() => {
    const fetchSessions = async () => {
      setLoadingSessions(true);
      try {
        // Fetch up to 10 for dashboard preview
        const data = await getAdminSessions(1, 10, '', '');
        setSessionsData(data || { items: [], total: 0 });
      } catch (err) {
        console.error('Failed to load sessions', err);
        setError('Failed to load sessions.');
        setSessionsData({ items: [], total: 0 });
      } finally {
        setLoadingSessions(false);
      }
    };
    fetchSessions();
  }, []);

  const completionRate = metrics?.total_sessions ? Math.round((metrics.completed_sessions / metrics.total_sessions) * 100) : 0;
  const avgDays = metrics?.avg_duration_hours ? (metrics.avg_duration_hours / 24).toFixed(1) : 0;

  // Helpers for table display mappings
  const determinePhase = (percent) => {
    if (percent === 100) return 'Graduated';
    if (percent > 70) return 'Security Review';
    if (percent > 30) return 'Codebase Deep Dive';
    return 'Environment Setup';
  };

  const determineStatus = (session) => {
    if (session.status === 'completed') return { label: 'COMPLETED', classes: 'text-teal-400 bg-teal-400/10 ring-teal-400/20' };
    
    // Simulate some variance based on percent
    if (session.percent_complete < 20 && session.percent_complete > 0) return { label: 'BLOCKED', classes: 'text-rose-500 bg-rose-500/10 ring-rose-500/20' };
    if (session.percent_complete === 45) return { label: 'AT RISK', classes: 'text-amber-400 bg-amber-400/10 ring-amber-400/20' };
    
    return { label: 'ON TRACK', classes: 'text-emerald-400 bg-emerald-400/10 ring-emerald-400/20' };
  };

  return (
    <div className="min-h-screen bg-[#0B0B0E] text-slate-400 font-sans flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 bg-[#0B0B0E] flex flex-col hidden md:flex">
        <div className="p-6 border-b border-white/5">
          <div className="flex items-center gap-2 font-semibold text-white text-lg tracking-wide">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
              O
            </div>
            O.N.E. <span className="text-indigo-500">Admin</span>
          </div>
        </div>
        
        <nav className="flex-1 px-4 space-y-2 mt-6 text-sm font-medium">
          <Link to="/dashboard" className="px-3 py-2.5 rounded-lg bg-indigo-600/10 text-indigo-400 flex items-center gap-3">
            <LayoutDashboard size={18} />
            Dashboard
          </Link>
          <Link to="/admin/developers" className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3">
            <Users size={18} />
            Developers
          </Link>
          <Link to="/admin/analytics" className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3">
            <BarChart2 size={18} />
            Analytics
          </Link>
        </nav>

        <div className="p-4 border-t border-white/5">
           <Link to="/admin/settings" className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-[#13131A] cursor-pointer transition-colors">
              <div className="w-8 h-8 rounded-full bg-indigo-600/20 flex flex-shrink-0 items-center justify-center text-indigo-400 text-xs font-bold">
                {adminProfile?.name ? adminProfile.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) : <UserIcon size={16} />}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">{adminProfile?.name || 'Loading...'}</p>
                <p className="text-xs text-slate-500 truncate capitalize">{adminProfile?.role?.replace('_', ' ') || '...'}</p>
              </div>
              <Settings size={16} className="text-slate-500" />
           </Link>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto overflow-x-hidden">
        {/* Header */}
        <header className="px-8 py-6 flex flex-col md:flex-row md:justify-between items-center gap-4">
           {/* Global Search */}
           <div className="relative w-full md:w-96">
             <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
             <input 
               type="text" 
               placeholder="Search developers, phases, or logs..." 
               className="w-full bg-[#13131A] text-sm text-white placeholder-slate-500 rounded-full pl-10 pr-4 py-2.5 outline-none border border-white/5 focus:border-indigo-500/50 transition-colors shadow-sm"
             />
           </div>
           {/* Header Actions */}
           <div className="flex items-center gap-5">
              <button className="relative text-slate-400 hover:text-white transition-colors">
                <Bell size={20} />
                <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-rose-500 rounded-full border-2 border-[#0B0B0E]"></span>
              </button>
              <button className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-5 py-2.5 rounded-full flex items-center gap-2 transition-colors shadow-lg shadow-indigo-600/20">
                <Plus size={16} strokeWidth={3} />
                Invite Developer
              </button>
           </div>
        </header>

        <div className="px-8 pb-12 space-y-8 max-w-7xl">
          {error && (
            <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm flex items-center gap-3">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          {/* KPI Metrics */}
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* KPI 1 */}
            <div className="bg-[#13131A] rounded-xl p-6 border border-white/5 relative overflow-hidden group hover:border-white/10 transition-colors">
               <div className="absolute -top-4 -right-4 p-8 opacity-[0.03] group-hover:opacity-10 transition-opacity">
                 <Users size={80} className="text-white" />
               </div>
               <div className="relative z-10">
                 <p className="text-slate-400 text-sm font-medium tracking-wide">Developers Onboarding</p>
                 <div className="mt-4 flex items-baseline gap-3">
                    <span className="text-3xl font-semibold text-white tracking-tight">
                      {loadingMetrics ? '...' : metrics?.active_sessions || 0}
                    </span>
                    <span className="text-emerald-400 text-sm font-medium flex items-center">
                      ↑ 2 this week
                    </span>
                 </div>
               </div>
            </div>

            {/* KPI 2 */}
            <div className="bg-[#13131A] rounded-xl p-6 border border-white/5 relative overflow-hidden group hover:border-white/10 transition-colors">
               <div className="absolute -top-4 -right-4 p-8 opacity-[0.03] group-hover:opacity-10 transition-opacity">
                 <Activity size={80} className="text-indigo-400" />
               </div>
               <div className="relative z-10">
                 <p className="text-slate-400 text-sm font-medium tracking-wide">Average Completion Rate</p>
                 <div className="mt-4 flex items-baseline gap-3">
                    <span className="text-3xl font-semibold text-indigo-400 tracking-tight">
                      {loadingMetrics ? '...' : `${completionRate}%`}
                    </span>
                    <span className="text-emerald-400 text-sm font-medium flex items-center">
                      ↑ 5%
                    </span>
                 </div>
               </div>
            </div>

            {/* KPI 3 */}
            <div className="bg-[#13131A] rounded-xl p-6 border border-white/5 relative overflow-hidden group hover:border-white/10 transition-colors">
               <div className="absolute -top-4 -right-4 p-8 opacity-[0.03] group-hover:opacity-10 transition-opacity">
                 <Clock size={80} className="text-white" />
               </div>
               <div className="relative z-10">
                 <p className="text-slate-400 text-sm font-medium tracking-wide">Avg. Time to Onboard</p>
                 <div className="mt-4 flex items-baseline gap-3">
                    <span className="text-3xl font-semibold text-white tracking-tight">
                      {loadingMetrics ? '...' : `${avgDays} days`}
                    </span>
                    <span className="text-rose-400 text-sm font-medium flex items-center">
                      ↓ 0.5d
                    </span>
                 </div>
               </div>
            </div>
          </section>

          {/* Critical Alert Banner */}
          <section className="bg-indigo-900/30 border border-indigo-500/30 rounded-xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-[0_0_20px_rgba(79,70,229,0.1)]">
             <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 flex-shrink-0 animate-pulse">
                  <AlertTriangle size={20} />
                </div>
                <div>
                   <h3 className="text-indigo-100 font-medium tracking-wide">Critical Status Update</h3>
                   <p className="text-indigo-300 text-sm mt-0.5">3 Developers are currently stuck on Environment Setup for more than 48 hours.</p>
                </div>
             </div>
             <button className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm px-5 py-2.5 rounded-lg font-medium whitespace-nowrap transition-colors flex-shrink-0 shadow-md">
               Investigate Now
             </button>
          </section>

          {/* Split Layout */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Left Column (Table) */}
            <div className="lg:col-span-2 bg-[#13131A] border border-white/5 rounded-xl flex flex-col overflow-hidden shadow-xl">
               <div className="px-6 py-5 border-b border-white/5 flex items-center justify-between">
                 <h2 className="text-white font-medium tracking-wide">Onboarding Progress</h2>
                 <div className="flex items-center gap-1 bg-[#0B0B0E] p-1 rounded-lg border border-white/5">
                    <button className="text-xs font-medium px-3 py-1.5 rounded-md bg-[#13131A] text-white shadow-sm border border-white/5">
                      All Phases
                    </button>
                    <button className="text-xs font-medium px-3 py-1.5 rounded-md text-slate-400 hover:text-white transition-colors">
                      Recent Only
                    </button>
                 </div>
               </div>
               
               <div className="overflow-x-auto flex-1">
                  <table className="w-full text-left text-sm whitespace-nowrap">
                    <thead className="bg-[#0B0B0E]/80 text-slate-500 text-xs uppercase tracking-wider font-semibold border-b border-white/5">
                      <tr>
                        <th className="px-6 py-4">Developer</th>
                        <th className="px-6 py-4">Current Phase</th>
                        <th className="px-6 py-4">Progress</th>
                        <th className="px-6 py-4 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      {loadingSessions ? (
                         <tr><td colSpan="4" className="px-6 py-12 text-center text-slate-500 tracking-widest text-xs uppercase animate-pulse">Scanning database...</td></tr>
                      ) : sessionsData.items.length === 0 ? (
                         <tr><td colSpan="4" className="px-6 py-12 text-center text-slate-500">No developers found.</td></tr>
                      ) : (
                        sessionsData.items.map(session => {
                           const statusObj = determineStatus(session);
                           const initial = session.employee_name ? session.employee_name.charAt(0).toUpperCase() : '?';
                           return (
                             <tr key={session.session_id} className="hover:bg-white/[0.02] transition-colors group">
                               <td className="px-6 py-4">
                                  <div className="flex items-center gap-3">
                                     <div className="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center text-indigo-300 font-semibold text-sm flex-shrink-0 border border-indigo-500/20 shadow-inner">
                                       {initial}
                                     </div>
                                     <div>
                                        <div className="text-white font-medium group-hover:text-indigo-400 transition-colors">
                                          <Link to={`/dashboard/sessions/${session.session_id}`}>
                                            {session.employee_name}
                                          </Link>
                                        </div>
                                        <div className="text-xs text-slate-500 mt-0.5">{session.role}</div>
                                     </div>
                                  </div>
                               </td>
                               <td className="px-6 py-4 text-slate-300 text-sm">
                                  {determinePhase(session.percent_complete)}
                               </td>
                               <td className="px-6 py-4">
                                  <div className="flex items-center gap-3 max-w-[140px]">
                                     <div className="flex-1 h-2 bg-[#0B0B0E] border border-white/5 rounded-full overflow-hidden">
                                        <div 
                                          className={`h-full rounded-full ${session.percent_complete === 100 ? 'bg-teal-400' : 'bg-indigo-500'} shadow-[0_0_10px_currentColor]`} 
                                          style={{ width: `${session.percent_complete}%` }}
                                        />
                                     </div>
                                     <span className="text-xs font-semibold text-slate-300 w-8">{session.percent_complete}%</span>
                                  </div>
                               </td>
                               <td className="px-6 py-4 text-right">
                                  <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-bold tracking-widest ring-1 ring-inset ${statusObj.classes}`}>
                                    {statusObj.label}
                                  </span>
                               </td>
                             </tr>
                           )
                        })
                      )}
                    </tbody>
                  </table>
               </div>
            </div>

            {/* Right Column (Analytics) */}
            <div className="space-y-8 flex flex-col h-full">
              {/* Chart Card */}
              <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl">
                 <div className="flex items-center justify-between mb-8">
                   <h3 className="text-white font-medium tracking-wide">Onboarding Volume</h3>
                   <MoreHorizontal size={18} className="text-slate-500 cursor-pointer hover:text-white transition-colors" />
                 </div>
                 {/* Mock Bar Chart */}
                 <div className="h-44 flex items-end justify-between gap-3 px-2">
                    {[4, 6, 9, 14, 11, 5, 3].map((val, idx) => (
                      <div key={idx} className="flex flex-col items-center gap-3 flex-1 group">
                         <div className="w-full bg-[#0B0B0E] border border-white/5 hover:border-white/10 transition-colors rounded-t-md flex items-end justify-center relative overflow-hidden h-full">
                            {/* The Bar */}
                            <div 
                              className="w-full bg-gradient-to-t from-indigo-900 to-indigo-500 rounded-t-sm transition-all duration-300 group-hover:to-indigo-400 group-hover:shadow-[0_0_15px_rgba(99,102,241,0.5)]" 
                              style={{ height: `${(val / 14) * 100}%` }}
                            />
                            {/* Tooltip */}
                            <div className="absolute -top-2 bg-[#13131A] border border-white/10 text-white text-[10px] font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity z-10 transform -translate-y-full">
                              {val}
                            </div>
                         </div>
                         <span className="text-[10px] text-slate-500 font-bold mt-1 tracking-widest">
                           {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][idx]}
                         </span>
                      </div>
                    ))}
                 </div>
              </div>

              {/* AI Insights Card */}
              <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 flex flex-col flex-1 shadow-xl">
                 <div className="flex items-center gap-2 mb-6">
                   <MessageSquare size={18} className="text-indigo-400" />
                   <h3 className="text-white font-medium tracking-wide">AI Assistant Insights</h3>
                 </div>
                 
                 <div className="space-y-6 flex-1">
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-4">Common Questions Asked</p>
                    
                    <div className="space-y-5">
                      {/* Insight Q1 */}
                      <div className="group">
                        <div className="flex justify-between text-sm mb-2">
                          <span className="text-slate-300 group-hover:text-white transition-colors">How to config VPN?</span>
                          <span className="text-slate-400 font-medium tabular-nums">42</span>
                        </div>
                        <div className="h-1.5 bg-[#0B0B0E] border border-white/5 rounded-full overflow-hidden">
                           <div className="h-full bg-indigo-500 w-[85%] rounded-full shadow-[0_0_8px_rgba(99,102,241,0.8)]"></div>
                        </div>
                      </div>

                      {/* Insight Q2 */}
                      <div className="group">
                        <div className="flex justify-between text-sm mb-2">
                          <span className="text-slate-300 group-hover:text-white transition-colors">Where are the AWS keys?</span>
                          <span className="text-slate-400 font-medium tabular-nums">28</span>
                        </div>
                        <div className="h-1.5 bg-[#0B0B0E] border border-white/5 rounded-full overflow-hidden">
                           <div className="h-full bg-indigo-400 w-[60%] rounded-full shadow-[0_0_8px_rgba(129,140,248,0.8)]"></div>
                        </div>
                      </div>

                      {/* Insight Q3 */}
                      <div className="group">
                        <div className="flex justify-between text-sm mb-2">
                          <span className="text-slate-300 group-hover:text-white transition-colors">Who to contact for Github access?</span>
                          <span className="text-slate-400 font-medium tabular-nums">15</span>
                        </div>
                        <div className="h-1.5 bg-[#0B0B0E] border border-white/5 rounded-full overflow-hidden">
                           <div className="h-full bg-indigo-300/80 w-[35%] rounded-full shadow-[0_0_8px_rgba(165,180,252,0.6)]"></div>
                        </div>
                      </div>
                    </div>
                 </div>

                 <button className="mt-8 w-full py-3 rounded-lg border border-white/5 bg-[#0B0B0E] text-slate-300 text-sm font-medium hover:bg-white/5 hover:text-white transition-colors flex items-center justify-center gap-2 shadow-sm">
                   View Chat Transcripts
                   <ArrowRight size={14} />
                 </button>
              </div>

            </div>
          </section>
        </div>

      </main>
    </div>
  );
};
