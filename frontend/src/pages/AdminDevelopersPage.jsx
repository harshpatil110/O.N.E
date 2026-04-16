import React, { useEffect, useState } from 'react';
import { getAdminSessions } from '../api/adminApi';
import { Link, useLocation } from 'react-router-dom';
import { 
  Search, Bell, Plus, AlertTriangle, ArrowRight,
  LayoutDashboard, Users, BarChart2, MessageSquare, Settings, User as UserIcon
} from 'lucide-react';

export const AdminDevelopersPage = () => {
  const [sessionsData, setSessionsData] = useState({ items: [], total: 0 });
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();

  useEffect(() => {
    let intervalId;
    const fetchSessions = async () => {
      try {
        const data = await getAdminSessions(1, 100, '', '');
        if (data) {
           setSessionsData(data);
        }
      } catch (err) {
        console.error('Failed to load sessions', err);
        setError('Failed to load developers.');
      } finally {
        setLoadingSessions(false);
      }
    };
    
    fetchSessions();
    intervalId = setInterval(fetchSessions, 5000);
    
    return () => clearInterval(intervalId);
  }, []);

  const determinePhase = (percent) => {
    if (percent === 0) return 'Awaiting Checklist';
    if (percent > 0 && percent <= 20) return 'Environment Setup';
    if (percent > 20 && percent <= 66) return 'Tooling & Access';
    return 'Security Training';
  };

  const determineStatus = (percent) => {
    if (percent === 0) return { label: 'JUST STARTED', classes: 'text-indigo-400 bg-indigo-400/10 ring-indigo-400/20' };
    if (percent > 0 && percent <= 20) return { label: 'BLOCKED', classes: 'text-rose-500 bg-rose-500/10 ring-rose-500/20' };
    return { label: 'ON TRACK', classes: 'text-emerald-400 bg-emerald-400/10 ring-emerald-400/20' };
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(date);
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
          <Link to="/dashboard" className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3">
            <LayoutDashboard size={18} />
            Dashboard
          </Link>
          <Link to="/admin/developers" className="px-3 py-2.5 rounded-lg bg-indigo-600/10 text-indigo-400 flex items-center gap-3">
            <Users size={18} />
            Developers
          </Link>
          <div className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3 cursor-pointer">
            <BarChart2 size={18} />
            Analytics
          </div>
          <div className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3 cursor-pointer">
            <MessageSquare size={18} />
            AI Insights
          </div>
        </nav>

        <div className="p-4 border-t border-white/5">
           <div className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-[#13131A] cursor-pointer transition-colors">
              <div className="w-8 h-8 rounded-full bg-slate-800 flex flex-shrink-0 items-center justify-center text-slate-300">
                <UserIcon size={16} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">Alex Chen</p>
                <p className="text-xs text-slate-500 truncate">Manager Mode</p>
              </div>
              <Settings size={16} className="text-slate-500" />
           </div>
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
              </button>
              <button className="px-5 py-2.5 rounded-full border border-indigo-500/50 text-indigo-400 text-sm font-medium hover:bg-indigo-500/10 transition-colors">
                View Analytics
              </button>
              <button className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-5 py-2.5 rounded-full flex items-center gap-2 transition-colors shadow-lg shadow-indigo-600/20">
                <Plus size={16} strokeWidth={3} />
                Invite
              </button>
           </div>
        </header>

        <div className="px-8 pb-12 w-full max-w-full">
          {error && (
            <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm flex items-center gap-3 mb-6">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          <div className="flex items-center justify-between mt-2 mb-8">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white mb-1">Developer Directory</h1>
              <p className="text-sm font-medium text-slate-500">Live overview of onboarding progression and access statuses.</p>
            </div>
          </div>

          {/* Full-width Data Table */}
          <div className="w-full bg-[#13131A] border border-white/5 rounded-xl shadow-xl overflow-hidden">
            <div className="overflow-x-auto w-full">
              <table className="w-full text-left text-sm whitespace-nowrap">
                <thead className="bg-[#0B0B0E]/80 text-slate-500 text-[11px] uppercase tracking-widest font-bold border-b border-white/5">
                  <tr>
                    <th className="px-6 py-4">Developer</th>
                    <th className="px-6 py-4">Start Date</th>
                    <th className="px-6 py-4">Current Phase</th>
                    <th className="px-6 py-4">Overall Progress</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {loadingSessions ? (
                    // Skeleton Loading
                    [...Array(5)].map((_, i) => (
                      <tr key={i} className="animate-pulse">
                        <td className="px-6 py-5 flex items-center gap-4">
                          <div className="w-10 h-10 rounded-full bg-white/5"></div>
                          <div className="space-y-2">
                            <div className="h-4 bg-white/5 rounded w-24"></div>
                            <div className="h-3 bg-white/5 rounded w-32"></div>
                          </div>
                        </td>
                        <td className="px-6 py-5"><div className="h-4 bg-white/5 rounded w-20"></div></td>
                        <td className="px-6 py-5"><div className="h-4 bg-white/5 rounded w-32"></div></td>
                        <td className="px-6 py-5">
                          <div className="flex items-center gap-3 w-40">
                            <div className="h-2 bg-white/5 rounded-full flex-1"></div>
                            <div className="h-4 bg-white/5 rounded w-6"></div>
                          </div>
                        </td>
                        <td className="px-6 py-5"><div className="h-6 bg-white/5 rounded w-20"></div></td>
                        <td className="px-6 py-5 text-right"><div className="h-4 bg-white/5 rounded w-16 ml-auto"></div></td>
                      </tr>
                    ))
                  ) : sessionsData.items.length === 0 ? (
                    <tr><td colSpan="6" className="px-6 py-16 text-center text-slate-500 font-medium">No developers found in database.</td></tr>
                  ) : (
                    sessionsData.items.map(session => {
                       const statusObj = determineStatus(session.percent_complete);
                       const name = session.employee_name || 'Unknown';
                       const email = session.user_email || `${name.toLowerCase().replace(' ', '')}@gmail.com`; // Fallback elegantly
                       const initial = name.charAt(0).toUpperCase();
                       
                       return (
                         <tr key={session.session_id} className="hover:bg-white/[0.02] transition-colors group">
                           <td className="px-6 py-5">
                              <div className="flex items-center gap-4">
                                 <div className="w-10 h-10 rounded-full bg-[#0B0B0E] flex items-center justify-center text-indigo-300 font-bold text-sm flex-shrink-0 border border-indigo-500/20 shadow-inner group-hover:border-indigo-500/50 transition-colors">
                                   {initial}
                                 </div>
                                 <div>
                                    <div className="text-white font-medium group-hover:text-indigo-400 transition-colors mb-0.5">
                                      {name}
                                    </div>
                                    <div className="text-xs font-medium text-slate-500">{email}</div>
                                 </div>
                              </div>
                           </td>
                           <td className="px-6 py-5 text-slate-300 font-medium font-mono text-[13px]">
                             {formatDate(session.started_at)}
                           </td>
                           <td className="px-6 py-5 text-slate-300 font-medium tracking-wide">
                              {determinePhase(session.percent_complete)}
                           </td>
                           <td className="px-6 py-5">
                              <div className="flex items-center gap-3 w-48">
                                 <div className="flex-1 h-2 bg-[#0B0B0E] border border-white/5 rounded-full overflow-hidden">
                                    <div 
                                      className="h-full bg-indigo-500 rounded-full shadow-[0_0_10px_currentColor] transition-all duration-500 ease-out" 
                                      style={{ width: `${session.percent_complete}%` }}
                                    />
                                 </div>
                                 <span className="text-[13px] font-bold text-slate-300 w-8">{session.percent_complete}%</span>
                              </div>
                           </td>
                           <td className="px-6 py-5">
                              <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-black tracking-widest ring-1 ring-inset ${statusObj.classes}`}>
                                {statusObj.label}
                              </span>
                           </td>
                           <td className="px-6 py-5 text-right">
                              <Link 
                                to={`/dashboard/sessions/${session.session_id}`} 
                                className="text-sm font-semibold text-indigo-400 hover:text-indigo-300 flex items-center justify-end gap-1.5 transition-colors group-hover:translate-x-0.5"
                              >
                                View Details
                                <ArrowRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                              </Link>
                           </td>
                         </tr>
                       )
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
};
