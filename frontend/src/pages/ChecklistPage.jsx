import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Link } from 'react-router-dom';
import { fetchTaskStates, submitTaskForVerification } from '../services/userService';

export const ChecklistPage = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [role, setRole] = useState('');
  const [loading, setLoading] = useState(true);
  const [submittingId, setSubmittingId] = useState(null);
  const [error, setError] = useState(null);

  const loadTasks = async () => {
    if (!user) return;
    try {
      const res = await fetchTaskStates(user.id);
      if (res.status === 'success') {
        setTasks(res.tasks);
        setRole(res.role || '');
      }
    } catch (err) {
      console.error('Failed to fetch task states', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial load
    loadTasks();
    
    // Silent background polling every 5 seconds
    const intervalId = setInterval(async () => {
      if (!user) return;
      try {
        const res = await fetchTaskStates(user.id);
        if (res.status === 'success') {
          setTasks(res.tasks);
          setRole(res.role || '');
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    }, 5000);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, [user]);

  const handleSubmitTask = async (taskId) => {
    setSubmittingId(taskId);
    setError(null);
    try {
      await submitTaskForVerification(taskId);
      // Immediately reflect in UI
      setTasks(prev => prev.map(t => 
        t.id === taskId ? { ...t, status: 'pending_verification' } : t
      ));
    } catch (err) {
      setError(err.message);
      console.error('Failed to submit task', err);
    } finally {
      setSubmittingId(null);
    }
  };

  // Calculate progress from DB state
  const verifiedCount = tasks.filter(t => t.status === 'verified').length;
  const totalCount = tasks.length;
  const progressPct = totalCount > 0 ? Math.round((verifiedCount / totalCount) * 100) : 0;

  if (loading) {
    return <div className="p-12 text-stone-900 font-sans h-full bg-[#F7F5F0]">Loading checklist...</div>;
  }

  if (tasks.length === 0) {
    return <div className="p-12 text-stone-900 font-sans h-full bg-[#F7F5F0]">No tasks found.</div>;
  }

  return (
    <div className="flex flex-col h-full overflow-y-auto bg-[#F7F5F0] text-stone-900 font-sans selection:bg-blue-100 relative">
      {/* Editorial Grid Pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40"
        style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, #E7E5E4 1px, transparent 0)',
          backgroundSize: '20px 20px'
        }}
      />
      
      {/* Header */}
      <div className="h-16 px-6 lg:px-12 flex items-center justify-between border-b border-stone-200 bg-[#F7F5F0]/90 backdrop-blur-sm z-10 sticky top-0">
        <div className="flex items-center gap-3">
          <div className="size-7 bg-stone-900 rounded-sm flex items-center justify-center text-stone-100 shadow-sm">
            <span className="font-bold font-mono text-xs tracking-tighter">O.</span>
          </div>
          <h2 className="text-stone-900 text-lg font-serif font-bold tracking-tight">O.N.E.</h2>
          <span className="text-[10px] font-mono uppercase tracking-widest text-stone-400 border-l border-stone-200 pl-3">Checklist</span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/chat" className="text-xs font-mono uppercase tracking-widest text-stone-500 hover:text-stone-900 transition-colors">
            Back to Chat
          </Link>
        </div>
      </div>

      <div className="max-w-3xl mx-auto w-full p-8 md:p-16 z-10">
        <header className="mb-16">
          <h1 className="text-4xl font-serif font-light tracking-tight mb-3">Onboarding Checklist</h1>
          <p className="text-xs font-mono uppercase tracking-widest text-stone-500">
            {role} &mdash; {progressPct}% Completed
          </p>
        </header>

        {error && (
          <div className="mb-6 p-4 border border-[#EAE1C5] bg-[#FDFBF2] text-[#917624] text-xs font-mono">
            ⚠ {error}
          </div>
        )}

        <div className="space-y-0">
          {tasks.map((task) => {
            const isVerified = task.status === 'verified';
            const isPending = task.status === 'pending_verification';
            const isActive = task.status === 'active';
            const isLocked = task.status === 'locked';

            return (
              <div 
                key={task.id} 
                className={`group flex items-start p-6 border-l pl-8 transition-all ${
                  isActive 
                    ? 'border-stone-900 bg-white/60 shadow-sm backdrop-blur-sm relative left-[-1px]' 
                    : isVerified 
                      ? 'border-stone-300 opacity-60' 
                      : isPending
                        ? 'border-[#917624] bg-[#FDFBF2]/30'
                        : 'border-stone-200 opacity-40'
                }`}
              >
                <div className="flex-1 pr-6">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-[10px] font-mono uppercase tracking-widest text-stone-400">Step {task.sequence}</span>
                    
                    {/* STATUS BADGES — driven by DB state */}
                    {isVerified && (
                      <span className="px-2 py-1 bg-[#F2EFE9] border border-[#E5E0D8] text-[#1A1A1A] text-[10px] font-mono uppercase tracking-widest">
                        Verified ✓
                      </span>
                    )}
                    {isPending && (
                      <span className="px-2 py-1 bg-[#FDFBF2] border border-[#EAE1C5] text-[#917624] text-[10px] font-mono uppercase tracking-widest animate-pulse">
                        Pending Verification
                      </span>
                    )}
                  </div>
                  <p className={`text-base md:text-lg font-light leading-relaxed ${
                    isVerified ? 'line-through text-stone-500' 
                    : isActive ? 'text-stone-900 font-normal' 
                    : isPending ? 'text-[#917624]'
                    : 'text-stone-600'
                  }`}>
                    {task.task_name}
                  </p>
                </div>
                
                {/* Active: Show clickable button */}
                {isActive && (
                  <button 
                    onClick={() => handleSubmitTask(task.id)}
                    disabled={submittingId === task.id}
                    className={`shrink-0 px-5 py-2.5 text-[10px] font-mono uppercase tracking-widest transition-colors rounded-sm shadow-sm ${
                      submittingId === task.id
                        ? 'bg-stone-400 text-stone-200 cursor-wait'
                        : 'bg-stone-900 text-[#F7F5F0] hover:bg-stone-800'
                    }`}
                  >
                    {submittingId === task.id ? 'Submitting...' : 'Mark as Done'}
                  </button>
                )}

                {/* Pending: Show awaiting badge */}
                {isPending && (
                  <span className="shrink-0 px-5 py-2.5 bg-[#FDFBF2] border border-[#EAE1C5] text-[#917624] text-[10px] font-mono uppercase tracking-widest">
                    Awaiting Admin
                  </span>
                )}

                {/* Locked: Show lock icon */}
                {isLocked && (
                  <div className="shrink-0 size-8 flex items-center justify-center pt-2">
                    <svg className="size-4 text-stone-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8V7z" />
                    </svg>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
