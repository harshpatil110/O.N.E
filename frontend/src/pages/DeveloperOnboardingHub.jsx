import React, { useState, useEffect } from 'react';
import { BookOpen, CheckCircle2, Circle, Clock, Code2, Database, GitBranch, MessageSquare, Terminal, UserSquare2, Briefcase, Users, LayoutDashboard, ChevronRight } from 'lucide-react';

const DeveloperOnboardingHub = () => {
  const [developerData, setDeveloperData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Mimicking a database fetch for 'harsh'
    const fetchData = async () => {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 800));

      const mockDbResponse = {
        developer: { 
            name: 'harsh', 
            role: 'React Native Developer', 
            joined: '10-02-2024', 
            progress: 20 
        },
        actions: [
            { title: 'Environment Setup Guide (React Native)', icon: 'Terminal' }, 
            { title: 'Access API Docs', icon: 'BookOpen' },
            { title: 'Local Setup Repository (Git)', icon: 'GitBranch' }
        ],
        tasks: [
            { id: 1, type: 'IT Setup', title: 'Configure laptop and accounts', complete: true }, 
            { id: 2, type: 'HR & Admin', title: 'Complete payroll forms', complete: false },
            { id: 3, type: 'HR & Admin', title: 'Read employee handbook', complete: false },
            { id: 4, type: 'Technical Setup', title: 'Setup Docker and local environment', complete: false },
            { id: 5, type: 'Technical Setup', title: 'Get Git access', complete: true },
            { id: 6, type: 'Training', title: 'Complete security module 1', complete: false }
        ],
        skills: [
            { name: 'React Native', proficiency: 2, max: 5 }, 
            { name: 'Docker', proficiency: 3, max: 5 },
            { name: 'APIs', proficiency: 1, max: 5 }
        ],
        project: { 
            name: 'Apollo Initiative', 
            role: 'Frontend Engineer',
            contact: 'Sarah Jenkins (Lead)',
            responsibilities: ['Mobile UI Development', 'API Integration', 'Performance Profiling'],
            progress: 35
        },
        log: [
            { id: 1, type: 'system', message: 'harsh completed security module 1.', time: '2 hrs ago' },
            { id: 2, type: 'human', message: 'HR sent a welcome message.', time: '5 hrs ago' },
            { id: 3, type: 'system', message: 'Setup Docker task assigned by mentor.', time: '1 day ago' },
            { id: 4, type: 'human', message: 'Joined the #apollo-frontend Slack channel.', time: '1 day ago' }
        ],
      };
      setDeveloperData(mockDbResponse);
      setIsLoading(false);
    };
    fetchData();
  }, []);

  if (isLoading) {
      return (
          <div className="min-h-screen bg-[#0B0B0E] flex flex-col items-center justify-center text-slate-400 font-sans">
              <div className="size-10 flex items-center justify-center animate-spin mb-4">
                  <div className="w-8 h-8 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full" />
              </div>
              <p className="text-sm font-bold tracking-widest uppercase text-indigo-400 animate-pulse">Loading Onboarding Matrix...</p>
          </div>
      );
  }

  const { developer, actions, tasks, skills, project, log } = developerData;

  const getIcon = (iconName) => {
      switch(iconName) {
          case 'Terminal': return <Terminal size={18} />;
          case 'BookOpen': return <BookOpen size={18} />;
          case 'GitBranch': return <GitBranch size={18} />;
          default: return <Code2 size={18} />;
      }
  };

  const tasksByType = tasks.reduce((acc, task) => {
      if (!acc[task.type]) acc[task.type] = [];
      acc[task.type].push(task);
      return acc;
  }, {});

  return (
    <div className="min-h-screen bg-[#0B0B0E] text-slate-300 font-sans p-6 md:p-10 flex justify-center">
        <div className="w-full max-w-7xl space-y-8">
            
            {/* Header: Developer Info */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 bg-[#13131A] p-8 rounded-2xl border border-white/5 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-500 to-emerald-400" />
                <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-2">
                        <UserSquare2 size={24} className="text-indigo-400" />
                        <h1 className="text-3xl font-extrabold text-white tracking-tight">{developer.name}</h1>
                        <span className="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 ml-2">
                            Active
                        </span>
                    </div>
                    <p className="text-slate-400 font-medium text-lg flex items-center gap-2">
                        {developer.role} <span className="text-slate-600">•</span> <span className="text-sm">Joined {developer.joined}</span>
                    </p>
                </div>
                <div className="relative z-10 flex gap-4">
                    <button className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg shadow-lg shadow-indigo-500/20 transition-all flex items-center gap-2">
                        <MessageSquare size={16} /> Contact Mentor
                    </button>
                </div>
            </div>

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
                                    <Clock size={16} className="text-indigo-400" /> Progression
                                </h3>
                                <p className="text-5xl font-black text-white tracking-tighter">
                                    {developer.progress}<span className="text-3xl text-slate-500">%</span>
                                </p>
                            </div>
                            <div className="text-right pb-1">
                                <span className="text-sm font-medium text-indigo-400 bg-indigo-400/10 px-3 py-1.5 rounded-lg border border-indigo-500/20">
                                    On Track
                                </span>
                            </div>
                        </div>
                        <div className="h-3 bg-[#0B0B0E] rounded-full overflow-hidden border border-white/5 relative z-10">
                            <div 
                                className="h-full bg-gradient-to-r from-indigo-500 to-[#22d3ee] transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(99,102,241,0.5)]"
                                style={{ width: `${developer.progress}%` }}
                            />
                        </div>
                    </div>

                    {/* Task Checklist Grouped Array */}
                    <div className="bg-[#13131A] p-8 rounded-2xl border border-white/5 shadow-xl">
                        <h3 className="text-lg font-bold text-white tracking-tight mb-6 flex items-center gap-2">
                            <LayoutDashboard size={20} className="text-indigo-400" /> Onboarding Checklist
                        </h3>
                        <div className="space-y-8">
                            {Object.entries(tasksByType).map(([type, checklist]) => (
                                <div key={type}>
                                    <h4 className="text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-3">
                                        {type}
                                        <div className="flex-1 h-px bg-white/5" />
                                    </h4>
                                    <div className="space-y-3">
                                        {checklist.map(task => (
                                            <div key={task.id} className="flex items-center gap-4 bg-[#0B0B0E]/50 p-4 rounded-xl border border-white/5 hover:border-slate-700 transition-colors group cursor-pointer">
                                                <div className="flex-shrink-0 mt-0.5">
                                                    {task.complete ? (
                                                        <CheckCircle2 size={20} className="text-emerald-400" />
                                                    ) : (
                                                        <Circle size={20} className="text-slate-600 group-hover:text-indigo-400 transition-colors" />
                                                    )}
                                                </div>
                                                <div className="flex-1">
                                                    <p className={`text-sm font-medium ${task.complete ? 'text-slate-500 line-through' : 'text-slate-200'}`}>
                                                        {task.title}
                                                    </p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Recommended Actions */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {actions.map((action, idx) => (
                            <div key={idx} className="bg-[#13131A] border border-white/5 p-5 rounded-xl hover:bg-[#1a1a24] transition-all cursor-pointer group">
                                <div className="size-10 bg-indigo-500/10 text-indigo-400 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                    {getIcon(action.icon)}
                                </div>
                                <h4 className="font-semibold text-white tracking-tight text-sm leading-snug pr-2 group-hover:text-indigo-300 transition-colors">{action.title}</h4>
                            </div>
                        ))}
                    </div>

                </div>

                {/* Right Column (Secondary Context) */}
                <div className="lg:col-span-4 space-y-8">
                    
                    {/* Project Assignment */}
                    <div className="bg-[#13131A] p-6 rounded-2xl border border-white/5 shadow-xl">
                        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-6">
                            <Briefcase size={16} className="text-emerald-400" /> Current Deployment
                        </h3>
                        <div className="mb-6">
                            <h2 className="text-xl font-bold text-white tracking-tight leading-tight">{project.name}</h2>
                            <p className="text-indigo-400 font-medium text-sm mt-1">{project.role}</p>
                        </div>
                        <div className="space-y-4 mb-6">
                            <h4 className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">Core Responsibilities</h4>
                            <ul className="space-y-2">
                                {project.responsibilities.map((resp, i) => (
                                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                                        <ChevronRight size={16} className="text-slate-600 mt-0.5 flex-shrink-0" />
                                        <span>{resp}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="pt-6 border-t border-white/5">
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 border border-slate-700">
                                    <Users size={14} />
                                </div>
                                <div>
                                    <p className="text-[10px] uppercase font-bold tracking-widest text-slate-500 mb-0.5">Team Lead</p>
                                    <p className="text-sm font-semibold text-white">{project.contact}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Technical Skills Matrix */}
                    <div className="bg-[#13131A] p-6 rounded-2xl border border-white/5 shadow-xl">
                        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-6">
                            <Database size={16} className="text-[#22d3ee]" /> Technical Matrix
                        </h3>
                        <div className="space-y-5">
                            {skills.map((skill, idx) => (
                                <div key={idx}>
                                    <div className="flex justify-between text-sm font-medium mb-2">
                                        <span className="text-white">{skill.name}</span>
                                        <span className="text-[#22d3ee]">Lvl {skill.proficiency}</span>
                                    </div>
                                    <div className="flex gap-1.5 h-2">
                                        {[...Array(skill.max)].map((_, i) => (
                                            <div 
                                                key={i} 
                                                className={`flex-1 rounded-full border transition-colors ${
                                                    i < skill.proficiency 
                                                        ? 'bg-[#22d3ee]/20 border-[#22d3ee]/50 shadow-[0_0_10px_rgba(34,211,238,0.2)]' 
                                                        : 'bg-white/5 border-transparent'
                                                }`} 
                                            />
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Communication Log */}
                    <div className="bg-[#13131A] p-6 rounded-2xl border border-white/5 shadow-xl flex flex-col h-[400px]">
                        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-6">
                            <MessageSquare size={16} className="text-rose-400" /> Event Stream
                        </h3>
                        <div className="flex-1 overflow-y-auto space-y-6 pr-2 custom-scrollbar">
                            <div className="relative before:absolute before:inset-0 before:ml-[5px] before:-translate-x-px before:h-full before:w-[1px] before:bg-white/5">
                                {log.map((entry, idx) => (
                                    <div key={entry.id} className="relative flex items-start gap-4 mb-6 last:mb-0">
                                        <div className={`absolute left-0 mt-1.5 size-2.5 rounded-full ${entry.type === 'human' ? 'bg-indigo-500 ring-4 ring-indigo-500/10' : 'bg-slate-700'}`} />
                                        <div className="pl-6 block">
                                            <p className="text-sm text-slate-300 font-medium leading-normal">{entry.message}</p>
                                            <time className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1 block">
                                                {entry.time}
                                            </time>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
  );
};

export default DeveloperOnboardingHub;
