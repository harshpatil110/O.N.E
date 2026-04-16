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
    <div className="flex h-screen bg-[#0a0a0c] text-white overflow-hidden font-sans selection:bg-[#4c6ef5]/30">
      
      {/* Background grid pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40 mix-blend-screen"
        style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0)',
          backgroundSize: '24px 24px'
        }}
      />

      {/* Global Left Sidebar */}
      <aside className="w-64 bg-[#111114] border-r border-[#1f1f23] flex flex-col z-10 hidden md:flex h-full">
        <div className="h-16 px-6 flex items-center border-b border-[#1f1f23] bg-transparent">
          <div className="flex items-center gap-2.5">
            <div className="size-7 bg-[#4c6ef5] rounded flex items-center justify-center text-white shadow-lg shadow-[#4c6ef5]/20">
              <span className="font-bold font-mono text-sm tracking-tighter">O.</span>
            </div>
            <h2 className="text-white text-lg font-extrabold tracking-tight">O.N.E</h2>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-6 scrollbar-hide">
          <div className="space-y-1">
            <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-2 mb-3">Onboarding Nav</h3>
            
            <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2 bg-[#4c6ef5]/10 text-[#4c6ef5] rounded-xl transition-colors font-medium text-sm group">
              <LayoutDashboard size={18} />
              Dashboard
            </Link>
            
            <Link to="/chat" className="flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
              <MessageSquare size={18} />
              Chat Assistant
            </Link>
             
             <Link to="#" className="flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
              <ListChecks size={18} />
              Checklist
            </Link>
             
              <Link to="/docs" className="flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
              <BookOpen size={18} />
              Docs
            </Link>
          </div>

          <div className="mt-auto space-y-3 pb-2">
            <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-2 mb-3">Integrations</h3>
             <button className="flex items-center gap-3 px-3 py-2 w-full text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
              <Code size={16} /> GitHub
            </button>
             <button className="flex items-center gap-3 px-3 py-2 w-full text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
              <MessageSquare size={16} /> Slack
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 lg:p-10 z-10">
         <div className="max-w-[1200px] mx-auto space-y-8">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
              <div>
                <h1 className="text-3xl font-extrabold tracking-tight text-white mb-2">
                  Welcome back, <span className="text-[#4c6ef5]">{user?.email ? user.email.split('@')[0] : 'Developer'}</span>.
                </h1>
                <p className="text-sm font-medium text-slate-400">Here's the status of your environment setup.</p>
              </div>
            </header>
            
            <div className="grid grid-cols-12 gap-8">
              {/* Center Panel: Progress & Actions & Tasks */}
              <div className="col-span-12 lg:col-span-8 space-y-8">
                  
                  {/* Progress Card */}
                  <section className="bg-[#111114]/40 border border-[#1f1f23] rounded-2xl p-8 backdrop-blur-sm relative overflow-hidden">
                    <div className="relative z-10">
                      <div className="flex items-end justify-between mb-6">
                        <div>
                           <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 flex items-center gap-2">
                             <Clock size={14} className="text-[#4c6ef5]" /> Onboarding Progress
                           </h4>
                           <h2 className="text-5xl font-black text-white tracking-tighter">
                             {loading ? '...' : Math.round(progress?.percent_complete || 0)}<span className="text-3xl text-slate-500">%</span>
                           </h2>
                        </div>
                        <div className="text-right">
                          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{progress?.completed_count || 0} / {progress?.total_items || 0} TASKS</p>
                        </div>
                      </div>
                      
                      <div className="h-3 w-full bg-white/5 rounded-full overflow-hidden border border-white/5">
                        <div 
                          className="h-full bg-[#4c6ef5] transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(76,110,245,0.8)]"
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

                      <div className="bg-[#111114]/30 border border-[#1f1f23] p-5 rounded-xl hover:border-slate-600 transition-all cursor-pointer group">
                        <div className="size-9 bg-white/5 text-slate-400 rounded-lg flex items-center justify-center mb-4 group-hover:bg-white/10 transition-colors border border-[#1f1f23]">
                          <BookOpen size={18} />
                        </div>
                        <h5 className="font-bold tracking-tight mb-1 text-sm">API Guides</h5>
                        <p className="text-[11px] text-slate-500 font-medium">Read through core engineering principles.</p>
                      </div>

                      <div className="bg-[#111114]/30 border border-[#1f1f23] p-5 rounded-xl hover:border-slate-600 transition-all cursor-pointer group">
                        <div className="size-9 bg-white/5 text-slate-400 rounded-lg flex items-center justify-center mb-4 group-hover:bg-white/10 transition-colors border border-[#1f1f23]">
                          <CheckSquare size={18} />
                        </div>
                        <h5 className="font-bold tracking-tight mb-1 text-sm">First Issue</h5>
                        <p className="text-[11px] text-slate-500 font-medium">Pick up your first 'good first issue'.</p>
                      </div>

                    </div>
                  </section>

                   {/* Active Tasks List */}
                  <section>
                     <div className="flex items-center justify-between mb-4">
                        <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Active Tasks</h4>
                     </div>
                     <div className="bg-[#111114]/40 border border-[#1f1f23] rounded-xl overflow-hidden backdrop-blur-sm">
                       {loading && progress.items.length === 0 ? (
                         <div className="p-8 text-center text-slate-500 text-xs font-bold uppercase tracking-widest">Loading tasks...</div>
                       ) : (progress.items.length > 0 ? progress.items : [
                          { id: 'd1', title: "Review Core Architecture ADRs", status: "pending", category: "Documentation" },
                          { id: 'd2', title: "Set up staging database credentials", status: "pending", category: "Environment" }
                       ]).filter(i => i.status !== 'completed').map((task, idx) => {
                           const isCompleted = task.status === 'completed';
                           if (isCompleted) return null; 

                           return (
                             <div key={task.id || idx} className="p-4 flex items-center gap-4 hover:bg-white/[0.02] transition-colors border-b border-[#1f1f23]">
                                <div className="flex-shrink-0">
                                   <div 
                                      onClick={() => toggleTask(task)}
                                      className="size-5 border-2 border-slate-600 rounded-md flex items-center justify-center hover:border-[#4c6ef5] cursor-pointer transition-colors"
                                   >
                                      {isCompleted && <Check size={12} className="text-[#4c6ef5]" />}
                                   </div>
                                </div>
                                <div className="flex-1 min-w-0">
                                   <h6 className="text-sm font-bold tracking-tight truncate">{task.title}</h6>
                                   <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-0.5 truncate">
                                     {task.category || 'General'} • PENDING
                                   </p>
                                </div>
                                {task.required && (
                                   <span className="px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-widest bg-amber-500/10 text-amber-500 border border-amber-500/20 whitespace-nowrap hidden sm:inline-block">High Priority</span>
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
                 <section className="bg-[#111114]/40 border border-[#1f1f23] rounded-xl p-6 shadow-sm backdrop-blur-sm h-full">
                    <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-8 flex items-center gap-2">
                       <History size={16} className="text-[#4c6ef5]" /> Recent Activity
                    </h4>
                    
                    <div className="space-y-8 relative before:absolute before:inset-0 before:ml-[5px] before:-translate-x-px before:h-full before:w-[1px] before:bg-[#1f1f23]">
                       <div className="relative flex items-start gap-4">
                         <div className="absolute left-0 mt-1.5 size-2.5 rounded-full bg-[#4c6ef5] ring-4 ring-[#4c6ef5]/10"></div>
                         <div className="pl-6">
                            <p className="text-xs font-bold tracking-tight text-white">System initiated <span className="text-[#4c6ef5]">Setup Profile</span></p>
                            <time className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mt-1 block">Just now</time>
                         </div>
                      </div>
                       {(progress.items.length > 0 ? progress.items : [
                          { id: 'd0', title: 'Configure local development environment', completed_at: new Date().toISOString(), status: 'completed' }
                       ]).filter(i => i.status === 'completed').map((task, idx) => (
                           <div key={task.id || idx} className="relative flex items-start gap-4">
                              <div className="absolute left-0 mt-1.5 size-2.5 rounded-full bg-slate-700"></div>
                              <div className="pl-6">
                                 <p className="text-xs font-bold tracking-tight text-white">Completed <span className="text-[#4c6ef5]">{task.title}</span></p>
                                 <time className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mt-1 block">
                                   {task.completed_at ? new Date(task.completed_at).toLocaleDateString() : 'Recently'}
                                 </time>
                              </div>
                           </div>
                         ))}
                    </div>

                    <div className="mt-12 p-4 bg-white/5 rounded-xl border border-white/10">
                       <h6 className="text-[9px] font-bold uppercase text-slate-500 tracking-widest mb-3">Onboarding Buddy</h6>
                       <div className="flex items-center gap-3">
                          <div className="size-9 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400">
                             <UserSquare2 size={18} />
                          </div>
                          <div>
                             <p className="text-xs font-black tracking-tight text-white">O.N.E. Agent</p>
                             <p className="text-[10px] font-medium text-slate-400 mt-0.5 tracking-tighter">AI Assistant</p>
                          </div>
                          <Link to="/chat" className="ml-auto size-8 bg-[#4c6ef5]/10 text-[#4c6ef5] rounded-lg flex items-center justify-center hover:bg-[#4c6ef5] hover:text-white transition-all border border-[#4c6ef5]/10">
                             <span className="material-symbols-outlined text-[16px]">chat</span>
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
