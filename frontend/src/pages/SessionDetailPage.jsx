import React, { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate, Link } from 'react-router-dom';
import { getProgress } from '../api/checklist';
import { getAdminSessions, resendHrNotification, toggleTaskCompletion } from '../api/adminApi';
import { ChatHistoryDrawer } from '../components/ChatHistoryDrawer';
import { 
    ArrowLeft, Mail, User as UserIcon, MessageSquareText, 
    Clock, CheckCircle2, Circle, Briefcase, Database, LayoutDashboard 
} from 'lucide-react';

export const SessionDetailPage = () => {
  const { sessionId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [sessionSummary, setSessionSummary] = useState(location.state?.sessionSummary || null);
  const [checklistData, setChecklistData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState('');
  const [drawerOpen, setDrawerOpen] = useState(false);

  useEffect(() => {
    const fetchSessionData = async () => {
      try {
        setLoading(true);

        const progressData = await getProgress(sessionId);
        setChecklistData(progressData);

        if (!sessionSummary) {
           const sessionsResp = await getAdminSessions(1, 100);
           const found = sessionsResp.items.find(s => s.session_id === sessionId);
           if (found) {
             setSessionSummary(found);
           }
        }
      } catch (err) {
        console.error(err);
        setError('Failed to fetch session details.');
      } finally {
        setLoading(false);
      }
    };
    fetchSessionData();
  }, [sessionId, sessionSummary]);

  const handleResend = async () => {
    try {
      setResending(true);
      await resendHrNotification(sessionId);
      alert('HR completion email sent successfully!');
    } catch (err) {
      console.error(err);
      alert('Failed to resend HR email.');
    } finally {
      setResending(false);
    }
  };

  const handleToggleTask = async (taskId, currentStatus) => {
    if (!checklistData) return;

    const isCurrentlyCompleted = currentStatus === 'completed';
    const newStatus = isCurrentlyCompleted ? 'pending' : 'completed';
    
    // OPTIMISTIC UPDATE
    const updatedItems = checklistData.items.map(item => {
      if (item.id === taskId) {
        return { 
          ...item, 
          status: newStatus,
          completed_at: newStatus === 'completed' ? new Date().toISOString() : null 
        };
      }
      return item;
    });

    const completedCount = updatedItems.filter(i => i.status === 'completed').length;
    const totalItems = updatedItems.length;
    const percentComplete = Math.round((completedCount / totalItems) * 100);

    const oldData = { ...checklistData };
    setChecklistData({
      ...checklistData,
      items: updatedItems,
      completed_count: completedCount,
      percent_complete: percentComplete
    });

    try {
      await toggleTaskCompletion(taskId, !isCurrentlyCompleted);
    } catch (err) {
      console.error("Failed to toggle task", err);
      setChecklistData(oldData);
      alert("Failed to update task status. Rolling back.");
    }
  };

  if (loading) {
      return (
          <div className="min-h-screen bg-[#0B0B0E] flex flex-col items-center justify-center text-slate-400 font-sans">
              <div className="size-10 flex items-center justify-center animate-spin mb-4">
                  <div className="w-8 h-8 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full" />
              </div>
              <p className="text-sm font-bold tracking-widest uppercase text-indigo-400 animate-pulse">Loading Session Details...</p>
          </div>
      );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0B0B0E] p-8 flex flex-col items-center justify-center">
        <div className="bg-rose-500/10 text-rose-400 p-4 rounded-xl border border-rose-500/20 max-w-md text-center">
          {error}
        </div>
        <button onClick={() => navigate('/admin/developers')} className="mt-6 text-indigo-400 hover:text-indigo-300 transition-colors uppercase tracking-widest text-sm font-bold flex items-center gap-2">
          <ArrowLeft size={16} /> Back to Directory
        </button>
      </div>
    );
  }

  const isCompleted = sessionSummary?.status === 'completed' || checklistData?.percent_complete === 100;

  return (
    <div className="min-h-screen bg-[#0B0B0E] text-slate-300 font-sans p-6 md:p-10 flex justify-center">
      <div className="w-full max-w-7xl space-y-8">
        
        {/* Navigation / Header Actions */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-white/5">
          <div className="space-y-4">
            <Link to="/admin/developers" className="inline-flex items-center gap-2 text-slate-500 hover:text-white font-medium text-sm transition-colors uppercase tracking-widest">
              <ArrowLeft size={16} /> Directory
            </Link>
            <h1 className="text-3xl font-extrabold text-white tracking-tight">Session Diagnostics</h1>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setDrawerOpen(true)}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#13131A] text-slate-300 text-sm font-bold border border-white/10 hover:bg-[#1a1a24] hover:text-white hover:border-slate-600 transition-all shadow-sm rounded-lg"
            >
              <MessageSquareText size={16} className="text-indigo-400" />
              View Conversation Log
            </button>

            {isCompleted && (
              <button
                onClick={handleResend}
                disabled={resending}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-lg shadow-lg shadow-indigo-500/20 hover:bg-indigo-500 disabled:opacity-50 transition-all"
              >
                <Mail size={16} />
                {resending ? 'Sending Email...' : 'Resend HR Email'}
              </button>
            )}
          </div>
        </div>

        {/* Employee Info Card */}
        {sessionSummary && (
          <div className="bg-[#13131A] p-8 rounded-2xl border border-white/5 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-500 to-emerald-400" />
            <div className="relative z-10 flex items-center gap-3 mb-6">
               <UserIcon size={20} className="text-indigo-400" />
               <h2 className="text-sm font-bold text-slate-500 uppercase tracking-widest">
                 Employee Information
               </h2>
               <span className="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 ml-auto">
                   Active Session
               </span>
            </div>
            
            <div className="relative z-10 grid grid-cols-1 md:grid-cols-4 gap-8">
               <div>
                 <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1.5">Name</div>
                 <div className="font-semibold text-xl text-white">{sessionSummary.employee_name}</div>
               </div>
               <div className="md:col-span-2">
                 <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1.5">Email / Identifier</div>
                 <div className="font-semibold text-lg text-slate-300">{sessionSummary.employee_email || `${sessionSummary.employee_name?.replace(' ', '').toLowerCase()}@gmail.com`}</div>
               </div>
               <div>
                 <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1.5">Role</div>
                 <div className="font-semibold text-lg text-slate-300">{sessionSummary.role || 'Developer'}</div>
               </div>
            </div>
          </div>
        )}

        {/* Dashboard Grid Container */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            {/* Left Column (Primary Tasks & Progress) */}
            <div className="lg:col-span-8 space-y-8">
                
                {/* Onboarding Progress Card */}
                <div className="bg-[#13131A] p-8 rounded-2xl border border-white/5 shadow-xl relative overflow-hidden group">
                    <div className="absolute inset-0 bg-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                    <div className="flex justify-between items-end mb-6 relative z-10">
                        <div>
                            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-2">
                                <Clock size={16} className="text-indigo-400" /> Administrative Tracker
                            </h3>
                            <p className="text-5xl font-black text-white tracking-tighter">
                                {checklistData?.percent_complete || 0}<span className="text-3xl text-slate-500">%</span>
                            </p>
                        </div>
                        <div className="text-right pb-1">
                            <span className="text-sm font-medium text-slate-400">
                                {checklistData?.completed_count || 0} / {checklistData?.total_items || 0} Complete
                            </span>
                        </div>
                    </div>
                    <div className="h-3 bg-[#0B0B0E] rounded-full overflow-hidden border border-white/5 relative z-10">
                        <div 
                            className="h-full bg-gradient-to-r from-indigo-500 to-[#22d3ee] transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(99,102,241,0.5)]"
                            style={{ width: `${checklistData?.percent_complete || 0}%` }}
                        />
                    </div>
                </div>

                {/* Task Checklist Array */}
                <div className="bg-[#13131A] p-8 rounded-2xl border border-white/5 shadow-xl">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                            <LayoutDashboard size={20} className="text-indigo-400" /> Onboarding Checklist
                        </h3>
                        <p className="text-[10px] text-emerald-400 font-bold uppercase tracking-widest bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
                            Admin Status Override
                        </p>
                    </div>
                    
                    <div className="space-y-3">
                        {checklistData?.items?.map(task => {
                            const isComplete = task.status === 'completed';
                            return (
                                <div 
                                    key={task.id} 
                                    onClick={() => handleToggleTask(task.id, task.status)}
                                    className="flex items-center gap-4 bg-[#0B0B0E]/50 p-4 rounded-xl border border-white/5 hover:border-indigo-500/30 transition-colors group cursor-pointer"
                                >
                                    <div className="flex-shrink-0 mt-0.5">
                                        {isComplete ? (
                                            <CheckCircle2 size={20} className="text-emerald-400" />
                                        ) : (
                                            <Circle size={20} className="text-slate-600 group-hover:text-indigo-400 transition-colors" />
                                        )}
                                    </div>
                                    <div className="flex-1">
                                        <p className={`text-sm font-medium transition-colors ${isComplete ? 'text-slate-500 line-through' : 'text-slate-200 group-hover:text-white'}`}>
                                            {task.title}
                                        </p>
                                    </div>
                                    <div className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">
                                        {isComplete ? 'Done' : 'Pending'}
                                    </div>
                                </div>
                            );
                        })}
                        {(!checklistData?.items || checklistData.items.length === 0) && (
                            <div className="bg-[#0B0B0E]/50 border border-white/5 p-8 rounded-xl text-center text-slate-500 text-sm font-bold tracking-widest uppercase">
                                No checklist items synced.
                            </div>
                        )}
                    </div>
                </div>

            </div>

            {/* Right Column (Secondary Context / Placeholders) */}
            <div className="lg:col-span-4 space-y-8">
                
                {/* Project Assignment */}
                <div className="bg-[#13131A] p-6 rounded-2xl border border-white/5 shadow-xl relative">
                    <h3 className="text-xs font-bold text-slate-600 uppercase tracking-widest flex items-center gap-2 mb-6">
                        <Briefcase size={16} className="text-slate-600" /> Current Deployment
                    </h3>
                    <div className="h-24 flex items-center justify-center border border-dashed border-white/10 rounded-xl bg-white/5">
                        <p className="text-[10px] tracking-widest font-bold uppercase text-slate-600">Awaiting Data Sync...</p>
                    </div>
                </div>

                {/* Technical Skills Matrix */}
                <div className="bg-[#13131A] p-6 rounded-2xl border border-white/5 shadow-xl relative">
                    <h3 className="text-xs font-bold text-slate-600 uppercase tracking-widest flex items-center gap-2 mb-6">
                        <Database size={16} className="text-slate-600" /> Technical Matrix
                    </h3>
                    <div className="h-32 flex items-center justify-center border border-dashed border-white/10 rounded-xl bg-white/5">
                        <p className="text-[10px] tracking-widest font-bold uppercase text-slate-600">Awaiting Data Sync...</p>
                    </div>
                </div>

                {/* Communication Log Placeholder Shell */}
                <div className="bg-[#13131A] p-6 rounded-2xl border border-white/5 shadow-xl relative flex flex-col h-[280px]">
                    <h3 className="text-xs font-bold text-slate-600 uppercase tracking-widest flex items-center gap-2 mb-6">
                        <MessageSquareText size={16} className="text-slate-600" /> Event Stream
                    </h3>
                    <div className="flex-1 flex items-center justify-center border border-dashed border-white/10 rounded-xl bg-white/5">
                        <p className="text-[10px] tracking-widest font-bold uppercase text-slate-600 text-center px-4">
                            Event logs are currently mapped out to the dedicated log drawer. <br/><br/>
                            <span className="text-indigo-400">Inline stream incoming next patch.</span>
                        </p>
                    </div>
                </div>

            </div>
        </div>
      </div>

      {/* Chat History Drawer */}
      <ChatHistoryDrawer
        isOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        sessionId={sessionId}
        employeeName={sessionSummary?.employee_name}
      />
    </div>
  );
};
