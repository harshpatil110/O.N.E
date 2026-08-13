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
          <div className="min-h-screen bg-[#F7F5F0] flex flex-col items-center justify-center text-stone-900 font-sans">
              <div className="size-8 flex items-center justify-center animate-spin mb-3">
                  <div className="w-6 h-6 border-2 border-stone-300 border-t-stone-900 rounded-full" />
              </div>
              <p className="text-xs font-mono uppercase tracking-widest text-stone-500">Loading Session Details...</p>
          </div>
      );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#F7F5F0] p-8 flex flex-col items-center justify-center">
        <div className="bg-rose-50 text-rose-800 p-4 rounded-sm border border-rose-200 max-w-md text-center text-xs font-mono">
          {error}
        </div>
        <button onClick={() => navigate('/admin/developers')} className="mt-6 text-stone-900 hover:text-stone-700 transition-colors uppercase tracking-widest text-xs font-mono font-bold flex items-center gap-2">
          <ArrowLeft size={14} /> Back to Directory
        </button>
      </div>
    );
  }

  const isCompleted = sessionSummary?.status === 'completed' || checklistData?.percent_complete === 100;

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-stone-900 font-sans p-6 md:p-10 flex justify-center">
      <div className="w-full max-w-7xl space-y-8">
        
        {/* Navigation / Header Actions */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-stone-200">
          <div className="space-y-3">
            <Link to="/admin/developers" className="inline-flex items-center gap-2 text-stone-500 hover:text-stone-900 font-mono text-xs transition-colors uppercase tracking-widest">
              <ArrowLeft size={14} /> Directory
            </Link>
            <h1 className="text-3xl font-serif font-bold text-stone-900 tracking-tight">Session Diagnostics</h1>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setDrawerOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white text-stone-900 text-xs font-medium border border-stone-300 hover:bg-stone-50 transition-colors shadow-sm rounded-sm"
            >
              <MessageSquareText size={14} className="text-stone-700" />
              View Conversation Log
            </button>

            {isCompleted && (
              <button
                onClick={handleResend}
                disabled={resending}
                className="inline-flex items-center gap-2 px-4 py-2 bg-stone-900 text-white text-xs font-mono font-bold uppercase tracking-wider rounded-sm shadow-sm hover:bg-stone-800 disabled:opacity-50 transition-colors"
              >
                <Mail size={14} />
                {resending ? 'Sending...' : 'Resend HR Email'}
              </button>
            )}
          </div>
        </div>

        {/* Employee Info Card */}
        {sessionSummary && (
          <div className="bg-white p-8 rounded-md border border-stone-200 shadow-sm relative overflow-hidden">
            <div className="relative z-10 flex items-center gap-3 mb-6">
               <UserIcon size={18} className="text-stone-700" />
               <h2 className="text-xs font-mono font-bold text-stone-500 uppercase tracking-widest">
                 Employee Information
               </h2>
               <span className="px-2.5 py-0.5 rounded-sm text-[10px] font-mono font-bold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-200 ml-auto">
                   Active Session
               </span>
            </div>
            
            <div className="relative z-10 grid grid-cols-1 md:grid-cols-4 gap-8">
               <div>
                 <div className="text-[10px] font-mono text-stone-400 uppercase tracking-widest mb-1">Name</div>
                 <div className="font-serif font-bold text-xl text-stone-900">{sessionSummary.employee_name}</div>
               </div>
               <div className="md:col-span-2">
                 <div className="text-[10px] font-mono text-stone-400 uppercase tracking-widest mb-1">Email / Identifier</div>
                 <div className="font-medium text-sm text-stone-700">{sessionSummary.employee_email || `${sessionSummary.employee_name?.replace(' ', '').toLowerCase()}@gmail.com`}</div>
               </div>
               <div>
                 <div className="text-[10px] font-mono text-stone-400 uppercase tracking-widest mb-1">Role</div>
                 <div className="font-medium text-sm text-stone-700">{sessionSummary.role || 'Developer'}</div>
               </div>
            </div>
          </div>
        )}

        {/* Dashboard Grid Container */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            {/* Left Column (Primary Tasks & Progress) */}
            <div className="lg:col-span-8 space-y-8">
                
                {/* Onboarding Progress Card */}
                <div className="bg-white p-8 rounded-md border border-stone-200 shadow-sm relative overflow-hidden group">
                    <div className="flex justify-between items-end mb-6 relative z-10">
                        <div>
                            <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-2">
                                <Clock size={14} className="text-stone-700" /> Administrative Tracker
                            </h3>
                            <p className="text-5xl font-serif font-bold text-stone-900 tracking-tight">
                                {checklistData?.percent_complete || 0}<span className="text-2xl text-stone-400 font-sans">%</span>
                            </p>
                        </div>
                        <div className="text-right pb-1">
                            <span className="text-xs font-mono font-medium text-stone-500">
                                {checklistData?.completed_count || 0} / {checklistData?.total_items || 0} Complete
                            </span>
                        </div>
                    </div>
                    <div className="h-2 bg-stone-100 rounded-sm overflow-hidden border border-stone-200 relative z-10">
                        <div 
                            className="h-full bg-stone-900 transition-all duration-700 ease-out"
                            style={{ width: `${checklistData?.percent_complete || 0}%` }}
                        />
                    </div>
                </div>

                {/* Task Checklist Array */}
                <div className="bg-white p-8 rounded-md border border-stone-200 shadow-sm">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-base font-serif font-bold text-stone-900 tracking-tight flex items-center gap-2">
                            <LayoutDashboard size={18} className="text-stone-700" /> Onboarding Checklist
                        </h3>
                        <p className="text-[9px] text-blue-900 font-mono font-bold uppercase tracking-widest bg-blue-100 px-2 py-0.5 rounded-sm border border-blue-200">
                            Admin Status Override
                        </p>
                    </div>
                    
                    <div className="space-y-2.5">
                        {checklistData?.items?.map(task => {
                            const isComplete = task.status === 'completed';
                            return (
                                <div 
                                    key={task.id} 
                                    onClick={() => handleToggleTask(task.id, task.status)}
                                    className="flex items-center gap-3 bg-[#F2F0EA]/50 p-3.5 rounded-sm border border-stone-200 hover:border-stone-400 transition-colors group cursor-pointer"
                                >
                                    <div className="flex-shrink-0 mt-0.5">
                                        {isComplete ? (
                                            <CheckCircle2 size={18} className="text-stone-900" />
                                        ) : (
                                            <Circle size={18} className="text-stone-400 group-hover:text-stone-800 transition-colors" />
                                        )}
                                    </div>
                                    <div className="flex-1">
                                        <p className={`text-xs font-medium transition-colors ${isComplete ? 'text-stone-400 line-through' : 'text-stone-800 group-hover:text-stone-950'}`}>
                                            {task.title}
                                        </p>
                                    </div>
                                    <div className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest">
                                        {isComplete ? 'Done' : 'Pending'}
                                    </div>
                                </div>
                            );
                        })}
                        {(!checklistData?.items || checklistData.items.length === 0) && (
                            <div className="bg-[#F2F0EA] border border-stone-200 p-8 rounded-sm text-center text-stone-400 font-mono text-xs uppercase">
                                No checklist items synced.
                            </div>
                        )}
                    </div>
                </div>

            </div>

            {/* Right Column */}
            <div className="lg:col-span-4 space-y-6">
                
                {/* Project Assignment */}
                <div className="bg-white p-6 rounded-md border border-stone-200 shadow-sm relative">
                    <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                        <Briefcase size={14} className="text-stone-400" /> Current Deployment
                    </h3>
                    <div className="h-20 flex items-center justify-center border border-dashed border-stone-200 rounded-sm bg-[#F2F0EA]/30">
                        <p className="text-[10px] font-mono uppercase tracking-widest text-stone-400">Awaiting Data Sync...</p>
                    </div>
                </div>

                {/* Technical Skills Matrix */}
                <div className="bg-white p-6 rounded-md border border-stone-200 shadow-sm relative">
                    <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                        <Database size={14} className="text-stone-400" /> Technical Matrix
                    </h3>
                    <div className="h-24 flex items-center justify-center border border-dashed border-stone-200 rounded-sm bg-[#F2F0EA]/30">
                        <p className="text-[10px] font-mono uppercase tracking-widest text-stone-400">Awaiting Data Sync...</p>
                    </div>
                </div>

                {/* Communication Log Placeholder */}
                <div className="bg-white p-6 rounded-md border border-stone-200 shadow-sm relative flex flex-col h-[240px]">
                    <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                        <MessageSquareText size={14} className="text-stone-400" /> Event Stream
                    </h3>
                    <div className="flex-1 flex items-center justify-center border border-dashed border-stone-200 rounded-sm bg-[#F2F0EA]/30 p-4">
                        <p className="text-[10px] font-mono uppercase tracking-widest text-stone-400 text-center">
                            Event logs mapped to dedicated drawer.
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
