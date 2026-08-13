import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Link } from 'react-router-dom';

export const ChecklistPage = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    if (!user) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/tasks/${user.id}`);
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [user]);

  const markComplete = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/tasks/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id }),
      });
      if (res.ok) {
        fetchTasks();
      }
    } catch (err) {
      console.error('Failed to complete task', err);
    }
  };

  if (loading) {
    return <div className="p-12 text-stone-900 font-sans h-full bg-[#F7F5F0]">Loading checklist...</div>;
  }

  if (!data) {
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
            {data.role} &mdash; {data.progress_percentage}% Completed
          </p>
        </header>

        <div className="space-y-0">
          {data.tasks_array.map((task, idx) => {
            const isCompleted = idx < data.tasks_completed;
            const isActive = idx === data.tasks_completed;
            const isLocked = idx > data.tasks_completed;

            return (
              <div 
                key={idx} 
                className={`group flex items-start p-6 border-l pl-8 transition-all ${
                  isActive 
                    ? 'border-stone-900 bg-white/60 shadow-sm backdrop-blur-sm relative left-[-1px]' 
                    : isCompleted 
                      ? 'border-stone-300 opacity-60' 
                      : 'border-stone-200 opacity-40'
                }`}
              >
                <div className="flex-1 pr-6">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-[10px] font-mono uppercase tracking-widest text-stone-400">Step {idx + 1}</span>
                    {isCompleted && (
                      <span className="text-[10px] font-mono uppercase tracking-widest text-green-700 bg-green-50 px-2 py-0.5 rounded-sm">Done</span>
                    )}
                  </div>
                  <p className={`text-base md:text-lg font-light leading-relaxed ${isCompleted ? 'line-through text-stone-500' : isActive ? 'text-stone-900 font-normal' : 'text-stone-600'}`}>
                    {task}
                  </p>
                </div>
                
                {isActive && (
                  <button 
                    onClick={markComplete}
                    className="shrink-0 px-5 py-2.5 bg-stone-900 text-[#F7F5F0] text-[10px] font-mono uppercase tracking-widest hover:bg-stone-800 transition-colors rounded-sm shadow-sm"
                  >
                    Mark as Done
                  </button>
                )}
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
