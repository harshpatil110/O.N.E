import React, { useEffect, useState } from 'react';
import { getAdminMetrics, getAdminSessions, getAdminAnalytics } from '../api/adminApi';
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
  const [analyticsData, setAnalyticsData] = useState([]);
  const [commonQuestions, setCommonQuestions] = useState([]);
  const [loadingMetrics, setLoadingMetrics] = useState(true);
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [error, setError] = useState(null);
  const [adminProfile, setAdminProfile] = useState(null);

  useEffect(() => {
      const fetchAdminProfile = async () => {
          try {
              const token = sessionStorage.getItem('token');
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
    
    const fetchAnalytics = async () => {
      try {
        const data = await getAdminAnalytics();
        // The API returns days starting from Monday maybe, let's just use what it returns.
        // It returns {"volume_data": [{"day": "Mon", "volume": 0}, ...]}
        // We'll map it to an array of objects to maintain the order returned.
        setAnalyticsData(data.volume_data || []);
        setCommonQuestions(data.common_questions || []);
      } catch (err) {
        console.error('Failed to load analytics', err);
      }
    };
    fetchAnalytics();
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
    if (session.status === 'completed') return { label: 'COMPLETED', classes: 'text-emerald-800 bg-emerald-100/80 border border-emerald-300' };
    
    // Simulate some variance based on percent
    if (session.percent_complete < 20 && session.percent_complete > 0) return { label: 'BLOCKED', classes: 'text-rose-800 bg-rose-100/80 border border-rose-300' };
    if (session.percent_complete === 45) return { label: 'AT RISK', classes: 'text-amber-800 bg-amber-100/80 border border-amber-300' };
    
    return { label: 'ON TRACK', classes: 'text-blue-800 bg-blue-100/80 border border-blue-300' };
  };

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-stone-900 font-sans flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-stone-200 bg-[#F2F0EA] flex flex-col hidden md:flex">
        <div className="p-6 border-b border-stone-200">
          <div className="flex items-center gap-2.5 font-serif font-bold text-stone-900 text-lg tracking-tight">
            <div className="w-7 h-7 rounded-sm bg-stone-900 flex items-center justify-center text-stone-100 font-mono text-xs">
              O
            </div>
            O.N.E. <span className="font-sans text-xs uppercase font-mono tracking-widest text-stone-400">Admin</span>
          </div>
        </div>
        
        <nav className="flex-1 px-4 space-y-1 mt-6 text-xs font-medium">
          <Link to="/admin" className="px-3 py-2.5 rounded-sm bg-stone-900 text-stone-100 flex items-center gap-3 shadow-sm">
            <LayoutDashboard size={16} />
            Dashboard
          </Link>
          <Link to="/admin/developers" className="px-3 py-2.5 rounded-sm text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 transition-colors flex items-center gap-3">
            <Users size={16} />
            Developers
          </Link>
          <Link to="/admin/analytics" className="px-3 py-2.5 rounded-sm text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 transition-colors flex items-center gap-3">
            <BarChart2 size={16} />
            Analytics
          </Link>
        </nav>

        <div className="p-4 border-t border-stone-200">
           <Link to="/admin/settings" className="flex items-center gap-3 px-2 py-2 rounded-sm hover:bg-stone-200/60 cursor-pointer transition-colors">
              <div className="w-7 h-7 rounded-sm bg-stone-200 flex flex-shrink-0 items-center justify-center text-stone-800 text-xs font-mono font-bold border border-stone-300">
                {adminProfile?.name ? adminProfile.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) : <UserIcon size={14} />}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-stone-900 truncate">{adminProfile?.name || 'Loading...'}</p>
                <p className="text-[10px] text-stone-500 font-mono truncate capitalize">{adminProfile?.role?.replace('_', ' ') || '...'}</p>
              </div>
              <Settings size={14} className="text-stone-400" />
           </Link>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto overflow-x-hidden">
        {/* Header */}
        <header className="px-8 py-6 flex flex-col md:flex-row md:justify-start items-center gap-4">
           {/* Header is clean now, preserving space for future breadcrumbs or titles */}
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
            <div className="bg-white rounded-md p-6 border border-stone-200 shadow-sm relative overflow-hidden group">
               <div className="relative z-10">
                 <p className="text-stone-500 text-[10px] font-mono uppercase tracking-widest font-semibold">Developers Onboarding</p>
                 <div className="mt-4 flex items-baseline gap-3">
                    <span className="text-4xl font-bold font-serif text-stone-900 tracking-tight">
                      {loadingMetrics ? '...' : metrics?.active_sessions || 0}
                    </span>
                    <span className="text-stone-500 text-xs font-mono">
                      ↑ 2 this week
                    </span>
                 </div>
               </div>
            </div>

            {/* KPI 2 */}
            <div className="bg-white rounded-md p-6 border border-stone-200 shadow-sm relative overflow-hidden group">
               <div className="relative z-10">
                 <p className="text-stone-500 text-[10px] font-mono uppercase tracking-widest font-semibold">Average Completion Rate</p>
                 <div className="mt-4 flex items-baseline gap-3">
                    <span className="text-4xl font-bold font-serif text-stone-900 tracking-tight">
                      {loadingMetrics ? '...' : `${completionRate}%`}
                    </span>
                    <span className="text-stone-500 text-xs font-mono">
                      ↑ 5%
                    </span>
                 </div>
               </div>
            </div>

            {/* KPI 3 */}
            <div className="bg-white rounded-md p-6 border border-stone-200 shadow-sm relative overflow-hidden group">
               <div className="relative z-10">
                 <p className="text-stone-500 text-[10px] font-mono uppercase tracking-widest font-semibold">Avg. Time to Onboard</p>
                 <div className="mt-4 flex items-baseline gap-3">
                    <span className="text-4xl font-bold font-serif text-stone-900 tracking-tight">
                      {loadingMetrics ? '...' : `${avgDays} days`}
                    </span>
                    <span className="text-stone-500 text-xs font-mono">
                      ↓ 0.5d
                    </span>
                 </div>
               </div>
            </div>
          </section>

          {/* Alert Banner */}
          <section className="bg-rose-50/80 border border-rose-200 rounded-md p-4 flex flex-col md:flex-row items-center justify-between gap-4">
             <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-sm bg-rose-100 flex items-center justify-center text-rose-800 flex-shrink-0 border border-rose-200">
                  <AlertTriangle size={16} />
                </div>
                <div>
                   <h3 className="text-rose-950 text-xs font-bold tracking-wide">Status Advisory</h3>
                   <p className="text-rose-800 text-xs mt-0.5">3 Developers are currently stuck on Environment Setup for more than 48 hours.</p>
                </div>
             </div>
             <button className="bg-stone-900 hover:bg-stone-800 text-white text-xs px-4 py-2 rounded-sm font-medium whitespace-nowrap transition-colors flex-shrink-0 shadow-sm">
               Investigate Now
             </button>
          </section>

          {/* Split Layout */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Left Column (Table) */}
            <div className="lg:col-span-2 bg-white border border-stone-200 rounded-md flex flex-col overflow-hidden shadow-sm">
               <div className="px-6 py-4 border-b border-stone-200 flex items-center justify-between bg-[#F2F0EA]/50">
                 <h2 className="text-stone-900 font-serif font-bold text-base tracking-tight">Onboarding Progress</h2>
               </div>
               
               <div className="overflow-x-auto flex-1">
                  <table className="w-full text-left text-xs whitespace-nowrap">
                    <thead className="bg-[#F2F0EA] text-stone-500 text-[10px] uppercase font-mono tracking-widest font-semibold border-b border-stone-200">
                      <tr>
                        <th className="px-6 py-3.5">Developer</th>
                        <th className="px-6 py-3.5">Current Phase</th>
                        <th className="px-6 py-3.5">Progress</th>
                        <th className="px-6 py-3.5 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-stone-100">
                      {loadingSessions ? (
                         <tr><td colSpan="4" className="px-6 py-12 text-center text-stone-400 font-mono text-xs uppercase">Scanning database...</td></tr>
                      ) : sessionsData.items.length === 0 ? (
                         <tr><td colSpan="4" className="px-6 py-12 text-center text-stone-400">No developers found.</td></tr>
                      ) : (
                        sessionsData.items.map(session => {
                           const statusObj = determineStatus(session);
                           const initial = session.employee_name ? session.employee_name.charAt(0).toUpperCase() : '?';
                           return (
                             <tr key={session.session_id} className="hover:bg-stone-50 transition-colors group">
                               <td className="px-6 py-4">
                                  <div className="flex items-center gap-3">
                                     <div className="w-8 h-8 rounded-sm bg-stone-100 flex items-center justify-center text-stone-800 font-mono font-bold text-xs flex-shrink-0 border border-stone-200">
                                       {initial}
                                     </div>
                                     <div>
                                        <div className="text-stone-900 font-medium group-hover:text-blue-800 transition-colors">
                                          <Link to={`/admin/sessions/${session.session_id}`}>
                                            {session.employee_name}
                                          </Link>
                                        </div>
                                        <div className="text-[11px] text-stone-500">{session.role}</div>
                                     </div>
                                  </div>
                               </td>
                               <td className="px-6 py-4 text-stone-600 font-medium">
                                  {determinePhase(session.percent_complete)}
                               </td>
                               <td className="px-6 py-4">
                                  <div className="flex items-center gap-3 max-w-[140px]">
                                     <div className="flex-1 h-1.5 bg-stone-100 border border-stone-200 rounded-sm overflow-hidden">
                                        <div 
                                          className={`h-full rounded-sm ${session.percent_complete === 100 ? 'bg-emerald-600' : 'bg-stone-900'}`} 
                                          style={{ width: `${session.percent_complete}%` }}
                                        />
                                     </div>
                                     <span className="text-xs font-mono font-semibold text-stone-700 w-8">{session.percent_complete}%</span>
                                  </div>
                               </td>
                               <td className="px-6 py-4 text-right">
                                  <span className={`inline-flex items-center px-2 py-0.5 rounded-sm text-[10px] font-mono font-bold tracking-wider ${statusObj.classes}`}>
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
            <div className="space-y-6 flex flex-col h-full">
              {/* Chart Card */}
              <div className="bg-white border border-stone-200 rounded-md p-6 shadow-sm">
                 <div className="flex items-center justify-between mb-6">
                   <h3 className="text-stone-900 font-serif font-bold text-sm tracking-tight">Onboarding Volume</h3>
                 </div>
                 {/* Dynamic Bar Chart */}
                 <div className="h-44 flex items-end justify-between gap-3 px-2">
                    {analyticsData.length > 0 ? analyticsData.map((item, idx) => {
                      const maxVolume = Math.max(...analyticsData.map(d => d.volume), 1);
                      return (
                      <div key={idx} className="flex flex-col items-center gap-2 flex-1 group">
                         <div className="w-full bg-stone-100 border border-stone-200 rounded-t-sm flex items-end justify-center relative overflow-hidden h-full">
                            {/* The Bar */}
                            <div 
                              className="w-full bg-stone-900 rounded-t-sm transition-all duration-300 group-hover:bg-blue-600" 
                              style={{ height: `${(item.volume / maxVolume) * 100}%` }}
                            />
                            {/* Tooltip */}
                            <div className="absolute -top-2 bg-stone-900 text-white text-[10px] font-mono px-2 py-0.5 rounded-sm opacity-0 group-hover:opacity-100 transition-opacity z-10 transform -translate-y-full">
                              {item.volume}
                            </div>
                         </div>
                         <span className="text-[10px] text-stone-500 font-mono tracking-wider">
                           {item.day}
                         </span>
                      </div>
                    )}) : (
                      <div className="w-full h-full flex items-center justify-center text-stone-400 text-xs font-mono">
                        Loading volume data...
                      </div>
                    )}
                 </div>
              </div>

              {/* AI Insights Card */}
              <div className="bg-white border border-stone-200 rounded-md p-6 flex flex-col flex-1 shadow-sm">
                 <div className="flex items-center gap-2 mb-6">
                   <MessageSquare size={16} className="text-stone-700" />
                   <h3 className="text-stone-900 font-serif font-bold text-sm tracking-tight">AI Assistant Insights</h3>
                 </div>
                 
                 <div className="space-y-5 flex-1">
                    <p className="text-[10px] font-mono uppercase tracking-widest text-stone-400 font-semibold mb-3">Common Developer Inquiries</p>
                    
                    <div className="space-y-4">
                      {commonQuestions.length > 0 ? commonQuestions.map((q, idx) => {
                        const maxCount = Math.max(...commonQuestions.map(cq => cq.count), 1);
                        const widthPct = Math.round((q.count / maxCount) * 100);
                        return (
                          <div key={idx} className="group">
                            <div className="flex justify-between text-xs mb-1.5">
                              <span className="text-stone-800 group-hover:text-stone-950 transition-colors truncate mr-4 font-medium">{q.question}</span>
                              <span className="text-stone-500 font-mono text-[11px] flex-shrink-0">{q.count}</span>
                            </div>
                            <div className="h-1 bg-stone-100 rounded-sm overflow-hidden border border-stone-200">
                               <div className="h-full bg-stone-800 rounded-sm" style={{ width: `${widthPct}%` }}></div>
                            </div>
                          </div>
                        );
                      }) : (
                        <p className="text-stone-400 text-xs font-mono">No inquiry data recorded.</p>
                      )}
                    </div>
                 </div>

                 <Link to="/admin/developers" className="mt-6 w-full py-2.5 rounded-sm border border-stone-200 bg-[#F2F0EA] text-stone-800 text-xs font-medium hover:bg-stone-200 transition-colors flex items-center justify-center gap-2">
                   View Chat Transcripts
                   <ArrowRight size={14} />
                 </Link>
              </div>

            </div>
          </section>
        </div>

      </main>
    </div>
  );
};
