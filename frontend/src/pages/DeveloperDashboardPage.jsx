import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { startSession } from '../api/chat';
import { getProgress, updateChecklistItem } from '../api/checklist';
import { Check, Clock, History, UserSquare2, Code, MessageSquare, Terminal, BookOpen, CheckSquare, LayoutDashboard, ListChecks } from 'lucide-react';

const DashboardContent = ({ sessionId }) => {
  const { user } = useAuth();
  const [progress, setProgress] = useState({ total_items: 0, completed_count: 0, percent_complete: 0, items: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (sessionId) {
      const fetchProgress = async () => {
        try {
          const data = await getProgress(sessionId);
          if (data && data.items) setProgress(data);
        } catch (e) {
          console.error("Failed to fetch progress", e);
        } finally {
          setLoading(false);
        }
      };
      fetchProgress();
      const interval = setInterval(fetchProgress, 5000);
      return () => clearInterval(interval);
    }
  }, [sessionId]);

  const toggleTask = async (task) => {
    if (task.status === 'completed') return; // For simplicity, don't un-mark here
    
    // Optimistic Update
    const updatedItems = [...progress.items];
    const index = updatedItems.findIndex(i => i.id === task.id);
    updatedItems[index].status = 'completed';
    setProgress(prev => ({ ...prev, items: updatedItems }));

    try {
      await updateChecklistItem(task.id, 'completed');
    } catch (e) {
      console.error(e); // rollback in real app
    }
  };

  return (
    <div className="flex h-screen bg-[#F7F5F0] text-stone-900 overflow-hidden font-sans selection:bg-blue-100">
      
      {/* Editorial Grid Pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40"
        style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, #E7E5E4 1px, transparent 0)',
          backgroundSize: '20px 20px'
        }}
      />

      {/* Global Left Sidebar */}
      <aside className="w-64 bg-[#F2F0EA] border-r border-stone-200 flex flex-col z-10 hidden md:flex h-full">
        <div className="h-16 px-6 flex items-center border-b border-stone-200 bg-transparent">
          <div className="flex items-center gap-2.5">
            <div className="size-7 bg-stone-900 rounded-sm flex items-center justify-center text-stone-100 shadow-sm">
              <span className="font-bold font-mono text-xs tracking-tighter">O.</span>
            </div>
            <h2 className="text-stone-900 text-lg font-serif font-bold tracking-tight">O.N.E.</h2>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-6">
          <div className="space-y-1">
            <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest pl-2 mb-2">Navigation</h3>
            
            <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2 bg-stone-900 text-stone-100 rounded-sm font-medium text-xs shadow-sm">
              <LayoutDashboard size={16} />
              Dashboard
            </Link>
            
            <Link to="/chat" className="flex items-center gap-3 px-3 py-2 text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 rounded-sm transition-colors font-medium text-xs">
              <MessageSquare size={16} />
              Chat Assistant
            </Link>
             
             <Link to="/docs" className="flex items-center gap-3 px-3 py-2 text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 rounded-sm transition-colors font-medium text-xs">
              <BookOpen size={16} />
              Docs
            </Link>
          </div>

          <div className="mt-auto space-y-2 pb-2">
            <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest pl-2 mb-2">Integrations</h3>
             <button className="flex items-center gap-3 px-3 py-2 w-full text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 rounded-sm transition-colors font-medium text-xs">
              <Code size={14} /> GitHub
            </button>
             <button className="flex items-center gap-3 px-3 py-2 w-full text-stone-600 hover:text-stone-900 hover:bg-stone-200/60 rounded-sm transition-colors font-medium text-xs">
              <MessageSquare size={14} /> Slack
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 lg:p-10 z-10">
         <div className="max-w-[1200px] mx-auto space-y-8">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
              <div>
                <h1 className="text-3xl font-serif font-bold tracking-tight text-stone-900 mb-1">
                  Welcome back, <span className="italic font-normal">{user?.email ? user.email.split('@')[0] : 'Developer'}</span>.
                </h1>
                <p className="text-xs font-mono uppercase tracking-widest text-stone-500">Overview of your environment setup and active tasks.</p>
              </div>
            </header>
            
            <div className="grid grid-cols-12 gap-8">
              {/* Center Panel: Progress & Actions & Tasks */}
              <div className="col-span-12 lg:col-span-8 space-y-8">
                  
                  {/* Progress Card */}
                  <section className="bg-white border border-stone-200 rounded-md p-8 shadow-sm relative overflow-hidden">
                    <div className="relative z-10">
                      <div className="flex items-end justify-between mb-6">
                        <div>
                           <h4 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest mb-1 flex items-center gap-2">
                             <Clock size={12} className="text-stone-700" /> Onboarding Progress
                           </h4>
                           <h2 className="text-5xl font-serif font-bold text-stone-900 tracking-tight">
                             {loading ? '...' : Math.round(progress?.percent_complete || 0)}<span className="text-2xl text-stone-400 font-sans">%</span>
                           </h2>
                        </div>
                        <div className="text-right">
                          <p className="text-[10px] font-mono font-bold text-stone-500 uppercase tracking-widest">{progress?.completed_count || 0} / {progress?.total_items || 0} TASKS</p>
                        </div>
                      </div>
                      
                      <div className="h-2 w-full bg-stone-100 rounded-sm overflow-hidden border border-stone-200">
                        <div 
                          className="h-full bg-stone-900 transition-all duration-700 ease-out"
                          style={{ width: `${progress?.percent_complete || 0}%` }}
                        />
                      </div>
                    </div>
                  </section>
                  
                  {/* Recommended Actions */}
                  <section>
                    <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Recommended Actions</h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      
                      <div className="bg-[#111114]/30 border border-[#1f1f23] p-5 rounded-xl hover:border-slate-600 transition-all cursor-pointer group">
                        <div className="size-9 bg-[#4c6ef5]/10 text-[#4c6ef5] rounded-lg flex items-center justify-center mb-4 group-hover:scale-105 transition-transform border border-[#4c6ef5]/20">
                          <Terminal size={18} />
                        </div>
                        <h5 className="font-bold tracking-tight mb-1 text-sm">Environment</h5>
                        <p className="text-[11px] text-slate-500 font-medium">Configure your local development toolchain.</p>
                      </div>

                      <div className="bg-white border border-stone-200 p-5 rounded-md hover:border-stone-400 transition-colors cursor-pointer group shadow-sm">
                        <div className="size-8 bg-stone-100 text-stone-800 rounded-sm flex items-center justify-center mb-3 group-hover:bg-stone-200 transition-colors border border-stone-200">
                          <BookOpen size={16} />
                        </div>
                        <h5 className="font-serif font-bold tracking-tight mb-1 text-sm text-stone-900">API Guides</h5>
                        <p className="text-[11px] text-stone-500 font-mono">Read through core engineering principles.</p>
                      </div>

                      <div className="bg-white border border-stone-200 p-5 rounded-md hover:border-stone-400 transition-colors cursor-pointer group shadow-sm">
                        <div className="size-8 bg-stone-100 text-stone-800 rounded-sm flex items-center justify-center mb-3 group-hover:bg-stone-200 transition-colors border border-stone-200">
                          <CheckSquare size={16} />
                        </div>
                        <h5 className="font-serif font-bold tracking-tight mb-1 text-sm text-stone-900">First Issue</h5>
                        <p className="text-[11px] text-stone-500 font-mono">Pick up your first 'good first issue'.</p>
                      </div>

                    </div>
                  </section>

                   {/* Active Tasks List */}
                  <section>
                     <div className="flex items-center justify-between mb-3">
                        <h4 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest">Active Tasks</h4>
                     </div>
                     <div className="bg-white border border-stone-200 rounded-md overflow-hidden shadow-sm">
                       {loading && progress.items.length === 0 ? (
                         <div className="p-8 text-center text-stone-400 font-mono text-xs uppercase">Loading tasks...</div>
                       ) : (progress.items.length > 0 ? progress.items : [
                          { id: 'd1', title: "Review Core Architecture ADRs", status: "pending", category: "Documentation" },
                          { id: 'd2', title: "Set up staging database credentials", status: "pending", category: "Environment" }
                       ]).filter(i => i.status !== 'completed').map((task, idx) => {
                           const isCompleted = task.status === 'completed';
                           if (isCompleted) return null; 

                           return (
                             <div key={task.id || idx} className="p-4 flex items-center gap-4 hover:bg-stone-50 transition-colors border-b border-stone-100">
                                <div className="flex-shrink-0">
                                   <div 
                                      onClick={() => toggleTask(task)}
                                      className="size-4 border border-stone-400 rounded-sm flex items-center justify-center hover:border-stone-900 cursor-pointer transition-colors bg-white"
                                   >
                                      {isCompleted && <Check size={10} className="text-stone-900" />}
                                   </div>
                                </div>
                                <div className="flex-1 min-w-0">
                                   <h6 className="text-xs font-semibold text-stone-900 truncate">{task.title}</h6>
                                   <p className="text-[10px] font-mono text-stone-400 uppercase tracking-widest mt-0.5 truncate">
                                     {task.category || 'General'} • PENDING
                                   </p>
                                </div>
                                {task.required && (
                                   <span className="px-2 py-0.5 rounded-sm text-[9px] font-mono font-bold uppercase tracking-widest bg-amber-100 text-amber-900 border border-amber-300 whitespace-nowrap hidden sm:inline-block">High Priority</span>
                                )}
                             </div>
                           )
                         })
                       }
                     </div>
                  </section>
              </div>

              {/* Right Column: Activity Timeline */}
              <div className="col-span-12 lg:col-span-4 space-y-8">
                 <section className="bg-white border border-stone-200 rounded-md p-6 shadow-sm h-full">
                    <h4 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest mb-6 flex items-center gap-2">
                       <History size={14} className="text-stone-700" /> Recent Activity
                    </h4>
                    
                    <div className="space-y-6 relative before:absolute before:inset-0 before:ml-[5px] before:-translate-x-px before:h-full before:w-[1px] before:bg-stone-200">
                       <div className="relative flex items-start gap-3">
                         <div className="absolute left-0 mt-1 size-2 rounded-full bg-stone-900 ring-2 ring-stone-200"></div>
                         <div className="pl-5">
                            <p className="text-xs font-semibold text-stone-900">System initiated <span className="font-serif italic text-stone-900">Setup Profile</span></p>
                            <time className="text-[9px] font-mono text-stone-400 uppercase tracking-widest mt-0.5 block">Just now</time>
                         </div>
                      </div>
                       {(progress.items.length > 0 ? progress.items : [
                          { id: 'd0', title: 'Configure local development environment', completed_at: new Date().toISOString(), status: 'completed' }
                       ]).filter(i => i.status === 'completed').map((task, idx) => (
                           <div key={task.id || idx} className="relative flex items-start gap-3">
                              <div className="absolute left-0 mt-1 size-2 rounded-full bg-stone-300"></div>
                              <div className="pl-5">
                                 <p className="text-xs font-medium text-stone-800">Completed <span className="font-medium text-stone-900">{task.title}</span></p>
                                 <time className="text-[9px] font-mono text-stone-400 uppercase tracking-widest mt-0.5 block">
                                   {task.completed_at ? new Date(task.completed_at).toLocaleDateString() : 'Recently'}
                                 </time>
                              </div>
                           </div>
                         ))}
                    </div>

                    <div className="mt-8 p-4 bg-[#F2F0EA] rounded-sm border border-stone-200">
                       <h6 className="text-[9px] font-mono font-bold uppercase text-stone-400 tracking-widest mb-2">Onboarding Mentor</h6>
                       <div className="flex items-center gap-3">
                          <div className="size-8 rounded-sm bg-stone-900 flex items-center justify-center text-stone-100 font-mono text-xs font-bold">
                             H
                          </div>
                          <div>
                             <p className="text-xs font-bold text-stone-900">Hermes AI</p>
                             <p className="text-[10px] font-mono text-stone-500">Supervisor Assistant</p>
                          </div>
                          <Link to="/chat" className="ml-auto px-3 py-1.5 bg-stone-900 text-stone-100 rounded-sm text-xs font-medium hover:bg-stone-800 transition-colors">
                             Chat
                          </Link>
                       </div>
                    </div>
                 </section>
              </div>
            </div>
         </div>
      </main>

    </div>
  );
};

export const DeveloperDashboardPage = () => {
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    const initData = async () => {
      try {
        const data = await startSession();
        setSessionId(data.session_id);
      } catch (e) {
        console.error(e);
      }
    };
    initData();
  }, []);

  return <DashboardContent sessionId={sessionId} />;
};
