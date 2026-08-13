import React, { useEffect, useState } from 'react';
import { getAdminSessions, getDeveloperChats } from '../api/adminApi';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { 
  Search, Bell, Plus, AlertTriangle, ArrowRight, X,
  LayoutDashboard, Users, BarChart2, MessageSquare, Settings, User as UserIcon
} from 'lucide-react';

export const AdminDevelopersPage = () => {
  const [sessionsData, setSessionsData] = useState({ items: [], total: 0 });
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [error, setError] = useState(null);
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
    if (percent === 0) return { label: 'JUST STARTED', classes: 'text-stone-700 bg-stone-100 border border-stone-300' };
    if (percent > 0 && percent <= 20) return { label: 'BLOCKED', classes: 'text-rose-800 bg-rose-100 border border-rose-300' };
    return { label: 'ON TRACK', classes: 'text-blue-800 bg-blue-100 border border-blue-300' };
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(date);
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
          <Link to="/admin" className="px-3 py-2.5 rounded-sm text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 transition-colors flex items-center gap-3">
            <LayoutDashboard size={16} />
            Dashboard
          </Link>
          <Link to="/admin/developers" className="px-3 py-2.5 rounded-sm bg-stone-900 text-stone-100 flex items-center gap-3 shadow-sm">
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
           {/* Header is clean now */}
        </header>

        <div className="px-8 pb-12 w-full max-w-full">
          {error && (
            <div className="bg-rose-50 border border-rose-200 text-rose-800 p-4 rounded-sm text-xs font-mono flex items-center gap-3 mb-6">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          <div className="flex items-center justify-between mt-2 mb-8">
            <div>
              <h1 className="text-2xl font-bold font-serif tracking-tight text-stone-900 mb-1">Developer Directory</h1>
              <p className="text-xs font-mono uppercase tracking-widest text-stone-500">Live overview of onboarding progression and access statuses.</p>
            </div>
          </div>

          {/* Full-width Data Table */}
          <div className="w-full bg-white border border-stone-200 rounded-md shadow-sm overflow-hidden">
            <div className="overflow-x-auto w-full">
              <table className="w-full text-left text-xs whitespace-nowrap">
                <thead className="bg-[#F2F0EA] text-stone-500 text-[10px] uppercase font-mono tracking-widest font-semibold border-b border-stone-200">
                  <tr>
                    <th className="px-6 py-3.5">Developer</th>
                    <th className="px-6 py-3.5">Start Date</th>
                    <th className="px-6 py-3.5">Current Phase</th>
                    <th className="px-6 py-3.5">Overall Progress</th>
                    <th className="px-6 py-3.5">Status</th>
                    <th className="px-6 py-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {loadingSessions ? (
                    [...Array(5)].map((_, i) => (
                      <tr key={i} className="animate-pulse">
                        <td className="px-6 py-4 flex items-center gap-3">
                          <div className="w-8 h-8 rounded-sm bg-stone-100"></div>
                          <div className="space-y-1">
                            <div className="h-3 bg-stone-100 rounded w-24"></div>
                            <div className="h-2 bg-stone-100 rounded w-32"></div>
                          </div>
                        </td>
                        <td className="px-6 py-4"><div className="h-3 bg-stone-100 rounded w-20"></div></td>
                        <td className="px-6 py-4"><div className="h-3 bg-stone-100 rounded w-32"></div></td>
                        <td className="px-6 py-4"><div className="h-3 bg-stone-100 rounded w-28"></div></td>
                        <td className="px-6 py-4"><div className="h-4 bg-stone-100 rounded w-16"></div></td>
                        <td className="px-6 py-4 text-right"><div className="h-3 bg-stone-100 rounded w-16 ml-auto"></div></td>
                      </tr>
                    ))
                  ) : sessionsData.items.length === 0 ? (
                    <tr><td colSpan="6" className="px-6 py-16 text-center text-stone-400 font-mono">No developers found in database.</td></tr>
                  ) : (
                    sessionsData.items.map(session => {
                       const statusObj = determineStatus(session.percent_complete);
                       const name = session.employee_name || 'Unknown';
                       const email = session.user_email || `${name.toLowerCase().replace(' ', '')}@gmail.com`;
                       const initial = name.charAt(0).toUpperCase();
                       
                       return (
                         <tr key={session.session_id} className="hover:bg-stone-50 transition-colors group">
                           <td className="px-6 py-4">
                              <div className="flex items-center gap-3">
                                 <div className="w-8 h-8 rounded-sm bg-stone-100 flex items-center justify-center text-stone-800 font-mono font-bold text-xs flex-shrink-0 border border-stone-200">
                                   {initial}
                                 </div>
                                 <div>
                                    <div className="text-stone-900 font-medium group-hover:text-blue-800 transition-colors mb-0.5">
                                      {name}
                                    </div>
                                    <div className="text-[11px] font-mono text-stone-400">{email}</div>
                                 </div>
                              </div>
                           </td>
                           <td className="px-6 py-4 text-stone-600 font-mono text-xs">
                             {formatDate(session.started_at)}
                           </td>
                           <td className="px-6 py-4 text-stone-700 font-medium">
                              {determinePhase(session.percent_complete)}
                           </td>
                           <td className="px-6 py-4">
                              <div className="flex items-center gap-3 w-44">
                                 <div className="flex-1 h-1.5 bg-stone-100 border border-stone-200 rounded-sm overflow-hidden">
                                    <div 
                                      className="h-full bg-stone-900 rounded-sm transition-all duration-300" 
                                      style={{ width: `${session.percent_complete}%` }}
                                    />
                                 </div>
                                 <span className="text-xs font-mono font-bold text-stone-700 w-8">{session.percent_complete}%</span>
                              </div>
                           </td>
                           <td className="px-6 py-4">
                              <span className={`inline-flex items-center px-2 py-0.5 rounded-sm text-[10px] font-mono font-bold tracking-wider ${statusObj.classes}`}>
                                {statusObj.label}
                              </span>
                           </td>
                           <td className="px-6 py-4 text-right">
                              <div className="flex items-center justify-end gap-3">
                                <button
                                  onClick={() => handleViewChats(session.user_id, name)}
                                  className="text-xs font-medium text-stone-600 hover:text-stone-900 flex items-center gap-1 transition-colors border border-stone-200 px-2.5 py-1 rounded-sm bg-stone-50"
                                >
                                  <MessageSquare size={13} />
                                  View Chats
                                </button>
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
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-stone-900/40 backdrop-blur-xs">
          <div className="bg-white border border-stone-200 rounded-md w-full max-w-2xl max-h-[85vh] flex flex-col shadow-lg">
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 bg-[#F2F0EA]">
              <div>
                <h2 className="text-base font-serif font-bold text-stone-900 flex items-center gap-2">
                  <MessageSquare size={16} className="text-stone-700" />
                  Chat Transcript
                </h2>
                <p className="text-xs font-mono text-stone-500">History with {selectedUserForChat}</p>
              </div>
              <button 
                onClick={() => setIsChatModalOpen(false)}
                className="text-stone-400 hover:text-stone-900 p-1.5 rounded-sm hover:bg-stone-200 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#F7F5F0]">
              {loadingChats ? (
                <div className="flex justify-center items-center h-40">
                  <div className="animate-spin rounded-full h-6 w-6 border-2 border-stone-400 border-t-stone-900"></div>
                </div>
              ) : chatTranscript.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-40 text-stone-400 font-mono text-xs space-y-2">
                  <MessageSquare size={24} className="opacity-30" />
                  <p>No chat history found for this developer.</p>
                </div>
              ) : (
                chatTranscript.map((chat) => {
                  const isAssistant = chat.role === 'assistant';
                  return (
                    <div key={chat.id} className={`flex w-full ${isAssistant ? 'justify-start' : 'justify-end'}`}>
                      <div className={`max-w-[80%] rounded-sm px-4 py-3 text-xs leading-relaxed ${
                        isAssistant 
                          ? 'bg-white text-stone-900 border border-stone-200 shadow-sm' 
                          : 'bg-[#BFDBFE] text-stone-900 border border-blue-300 shadow-sm'
                      }`}>
                        <div className="flex items-center gap-2 mb-1 text-[10px] font-mono uppercase tracking-wider text-stone-500">
                          <span>{isAssistant ? 'O.N.E. Assistant' : selectedUserForChat}</span>
                          <span>•</span>
                          <span>{formatDate(chat.created_at)}</span>
                        </div>
                        <div className="text-xs whitespace-pre-wrap font-sans">
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
