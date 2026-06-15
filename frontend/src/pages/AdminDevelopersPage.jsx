import React, { useEffect, useState } from 'react';
import { getAdminSessions, getDeveloperChats } from '../api/adminApi';
import axios from 'axios';
import { Link, useLocation } from 'react-router-dom';
import { 
  Search, Bell, Plus, AlertTriangle, ArrowRight, X,
  LayoutDashboard, Users, BarChart2, MessageSquare, Settings, User as UserIcon
} from 'lucide-react';

export const AdminDevelopersPage = () => {
  const [sessionsData, setSessionsData] = useState({ items: [], total: 0 });
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [adminProfile, setAdminProfile] = useState(null);

  const [selectedUserForChat, setSelectedUserForChat] = useState(null);
  const [chatTranscript, setChatTranscript] = useState([]);
  const [loadingChats, setLoadingChats] = useState(false);
  const [isChatModalOpen, setIsChatModalOpen] = useState(false);

  const handleViewChats = async (user_id, name) => {
    setSelectedUserForChat(name);
    setIsChatModalOpen(true);
    setLoadingChats(true);
    setChatTranscript([]);
    try {
      const data = await getDeveloperChats(user_id);
      setChatTranscript(data.chats || []);
    } catch (err) {
      console.error('Failed to load chats', err);
      // Let it be empty so the empty state handles it
    } finally {
      setLoadingChats(false);
    }
  };

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
          <Link to="/admin" className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3">
            <LayoutDashboard size={18} />
            Dashboard
          </Link>
          <Link to="/admin/developers" className="px-3 py-2.5 rounded-lg bg-indigo-600/10 text-indigo-400 flex items-center gap-3">
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
                              <div className="flex items-center justify-end gap-4">
                                <button
                                  onClick={() => handleViewChats(session.user_id, name)}
                                  className="text-sm font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors"
                                >
                                  <MessageSquare size={14} />
                                  View Chats
                                </button>
                                <Link 
                                  to={`/dashboard/sessions/${session.session_id}`} 
                                  className="text-sm font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1.5 transition-colors group-hover:translate-x-0.5"
                                >
                                  View Details
                                  <ArrowRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                                </Link>
                              </div>
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

      {/* Chat Transcript Modal */}
      {isChatModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#111114] border border-[#1f1f23] rounded-2xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <MessageSquare size={18} className="text-indigo-400" />
                  Chat Transcript
                </h2>
                <p className="text-sm text-slate-500">History with {selectedUserForChat}</p>
              </div>
              <button 
                onClick={() => setIsChatModalOpen(false)}
                className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-white/5 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {loadingChats ? (
                <div className="flex justify-center items-center h-40">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
                </div>
              ) : chatTranscript.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-40 text-slate-500 space-y-3">
                  <MessageSquare size={32} className="opacity-20" />
                  <p>No chat history found for this developer.</p>
                </div>
              ) : (
                chatTranscript.map((chat) => {
                  const isAssistant = chat.role === 'assistant';
                  return (
                    <div key={chat.id} className={`flex w-full ${isAssistant ? 'justify-start' : 'justify-end'}`}>
                      <div className={`max-w-[80%] rounded-2xl px-5 py-3.5 ${
                        isAssistant 
                          ? 'bg-[#1a1a24] text-slate-300 border border-white/5 rounded-tl-sm' 
                          : 'bg-indigo-600 text-white rounded-tr-sm shadow-lg shadow-indigo-500/20'
                      }`}>
                        <div className="flex items-center gap-2 mb-1 opacity-70 text-[11px] font-medium uppercase tracking-wider">
                          {isAssistant ? 'O.N.E. Assistant' : selectedUserForChat}
                          <span className="opacity-50">•</span>
                          <span>{formatDate(chat.created_at)}</span>
                        </div>
                        <div className="text-sm leading-relaxed whitespace-pre-wrap">
                          {chat.content}
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
