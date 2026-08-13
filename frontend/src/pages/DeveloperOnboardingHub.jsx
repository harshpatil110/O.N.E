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
          <div className="min-h-screen bg-[#F7F5F0] flex flex-col items-center justify-center text-stone-900 font-sans">
              <div className="size-8 flex items-center justify-center animate-spin mb-3">
                  <div className="w-6 h-6 border-2 border-stone-300 border-t-stone-900 rounded-full" />
              </div>
              <p className="text-xs font-mono uppercase tracking-widest text-stone-500">Loading Onboarding Matrix...</p>
          </div>
      );
  }

  const { developer, actions, tasks, skills, project, log } = developerData;

  const getIcon = (iconName) => {
      switch(iconName) {
          case 'Terminal': return <Terminal size={16} />;
          case 'BookOpen': return <BookOpen size={16} />;
          case 'GitBranch': return <GitBranch size={16} />;
          default: return <Code2 size={16} />;
      }
  };

  const tasksByType = tasks.reduce((acc, task) => {
      if (!acc[task.type]) acc[task.type] = [];
      acc[task.type].push(task);
      return acc;
  }, {});

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-stone-900 font-sans p-6 md:p-10 flex justify-center selection:bg-blue-100">
        <div className="w-full max-w-7xl space-y-8">
            
            {/* Header: Developer Info */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 bg-white p-8 rounded-md border border-stone-200 shadow-sm relative overflow-hidden">
                <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-1.5">
                        <UserSquare2 size={20} className="text-stone-700" />
                        <h1 className="text-3xl font-serif font-bold text-stone-900 tracking-tight">{developer.name}</h1>
                        <span className="px-2.5 py-0.5 rounded-sm text-[10px] font-mono font-bold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-200 ml-2">
                            Active
                        </span>
                    </div>
                    <p className="text-stone-500 font-medium text-sm flex items-center gap-2">
                        {developer.role} <span className="text-stone-300">•</span> <span className="text-xs font-mono">Joined {developer.joined}</span>
                    </p>
                </div>
                <div className="relative z-10 flex gap-4">
                    <button className="px-4 py-2 bg-stone-900 hover:bg-stone-800 text-white text-xs font-mono font-bold uppercase tracking-wider rounded-sm shadow-sm transition-colors flex items-center gap-2">
                        <MessageSquare size={14} /> Contact Mentor
                    </button>
                </div>
            </div>

            {/* Dashboard Grid Container */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                {/* Left Column (Primary Tasks & Progress) */}
                <div className="lg:col-span-8 space-y-8">
                    
                    {/* Onboarding Progress Card */}
                    <div className="bg-white p-8 rounded-md border border-stone-200 shadow-sm relative overflow-hidden group">
                        <div className="flex justify-between items-end mb-6 relative z-10">
                            <div>
                                <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-2">
                                    <Clock size={14} className="text-stone-700" /> Progression
                                </h3>
                                <p className="text-5xl font-serif font-bold text-stone-900 tracking-tight">
                                    {developer.progress}<span className="text-2xl text-stone-400 font-sans">%</span>
                                </p>
                            </div>
                            <div className="text-right pb-1">
                                <span className="text-xs font-mono font-bold uppercase tracking-widest text-stone-700 bg-stone-100 px-3 py-1.5 rounded-sm border border-stone-200">
                                    On Track
                                </span>
                            </div>
                        </div>
                        <div className="h-2 bg-stone-100 rounded-sm overflow-hidden border border-stone-200 relative z-10">
                            <div 
                                className="h-full bg-stone-900 transition-all duration-700 ease-out"
                                style={{ width: `${developer.progress}%` }}
                            />
                        </div>
                    </div>

                    {/* Task Checklist Grouped Array */}
                    <div className="bg-white p-8 rounded-md border border-stone-200 shadow-sm">
                        <h3 className="text-base font-serif font-bold text-stone-900 tracking-tight mb-6 flex items-center gap-2">
                            <LayoutDashboard size={18} className="text-stone-700" /> Onboarding Checklist
                        </h3>
                        <div className="space-y-6">
                            {Object.entries(tasksByType).map(([type, checklist]) => (
                                <div key={type}>
                                    <h4 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest mb-3 flex items-center gap-3">
                                        {type}
                                        <div className="flex-1 h-px bg-stone-200" />
                                    </h4>
                                    <div className="space-y-2">
                                        {checklist.map(task => (
                                            <div key={task.id} className="flex items-center gap-3 bg-[#F2F0EA]/50 p-3.5 rounded-sm border border-stone-200 hover:border-stone-400 transition-colors group cursor-pointer">
                                                <div className="flex-shrink-0 mt-0.5">
                                                    {task.complete ? (
                                                        <CheckCircle2 size={18} className="text-stone-900" />
                                                    ) : (
                                                        <Circle size={18} className="text-stone-400 group-hover:text-stone-800 transition-colors" />
                                                    )}
                                                </div>
                                                <div className="flex-1">
                                                    <p className={`text-xs font-medium ${task.complete ? 'text-stone-400 line-through' : 'text-stone-800'}`}>
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
                            <div key={idx} className="bg-white border border-stone-200 p-5 rounded-md hover:border-stone-900 transition-colors cursor-pointer group shadow-sm">
                                <div className="size-8 bg-stone-100 text-stone-800 rounded-sm flex items-center justify-center mb-3 group-hover:bg-stone-200 transition-colors border border-stone-200">
                                    {getIcon(action.icon)}
                                </div>
                                <h4 className="font-serif font-bold text-stone-900 tracking-tight text-xs leading-snug pr-2 group-hover:text-blue-800 transition-colors">{action.title}</h4>
                            </div>
                        ))}
                    </div>

                </div>

                {/* Right Column (Secondary Context) */}
                <div className="lg:col-span-4 space-y-8">
                    
                    {/* Project Assignment */}
                    <div className="bg-white p-6 rounded-md border border-stone-200 shadow-sm">
                        <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                            <Briefcase size={14} className="text-stone-700" /> Current Deployment
                        </h3>
                        <div className="mb-4">
                            <h2 className="text-lg font-serif font-bold text-stone-900 tracking-tight">{project.name}</h2>
                            <p className="text-xs font-mono text-blue-800 font-bold mt-0.5">{project.role}</p>
                        </div>
                        <div className="space-y-3 mb-6">
                            <h4 className="text-[9px] font-mono font-bold text-stone-400 uppercase tracking-widest">Core Responsibilities</h4>
                            <ul className="space-y-1.5">
                                {project.responsibilities.map((resp, i) => (
                                    <li key={i} className="flex items-start gap-2 text-xs text-stone-700">
                                        <ChevronRight size={14} className="text-stone-400 mt-0.5 flex-shrink-0" />
                                        <span>{resp}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="pt-4 border-t border-stone-100">
                            <div className="flex items-center gap-3">
                                <div className="w-7 h-7 rounded-sm bg-stone-100 flex items-center justify-center text-stone-800 font-mono text-xs border border-stone-200">
                                    <Users size={14} />
                                </div>
                                <div>
                                    <p className="text-[9px] font-mono uppercase font-bold tracking-widest text-stone-400">Team Lead</p>
                                    <p className="text-xs font-bold text-stone-900">{project.contact}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Technical Skills Matrix */}
                    <div className="bg-white p-6 rounded-md border border-stone-200 shadow-sm">
                        <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                            <Database size={14} className="text-stone-700" /> Technical Matrix
                        </h3>
                        <div className="space-y-4">
                            {skills.map((skill, idx) => (
                                <div key={idx}>
                                    <div className="flex justify-between text-xs font-medium mb-1.5">
                                        <span className="text-stone-900">{skill.name}</span>
                                        <span className="text-stone-500 font-mono text-[10px]">Lvl {skill.proficiency}</span>
                                    </div>
                                    <div className="flex gap-1 h-1.5">
                                        {[...Array(skill.max)].map((_, i) => (
                                            <div 
                                                key={i} 
                                                className={`flex-1 rounded-sm border transition-colors ${
                                                    i < skill.proficiency 
                                                        ? 'bg-stone-900 border-stone-900' 
                                                        : 'bg-stone-100 border-stone-200'
                                                }`} 
                                            />
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Communication Log */}
                    <div className="bg-white p-6 rounded-md border border-stone-200 shadow-sm flex flex-col h-[360px]">
                        <h3 className="text-[10px] font-mono font-bold text-stone-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                            <MessageSquare size={14} className="text-stone-700" /> Event Stream
                        </h3>
                        <div className="flex-1 overflow-y-auto space-y-4 pr-1">
                            <div className="relative before:absolute before:inset-0 before:ml-[4px] before:-translate-x-px before:h-full before:w-[1px] before:bg-stone-200">
                                {log.map((entry) => (
                                    <div key={entry.id} className="relative flex items-start gap-3 mb-4 last:mb-0">
                                        <div className={`absolute left-0 mt-1 size-2 rounded-full ${entry.type === 'human' ? 'bg-stone-900 ring-2 ring-stone-200' : 'bg-stone-300'}`} />
                                        <div className="pl-4 block">
                                            <p className="text-xs text-stone-800 font-medium leading-normal">{entry.message}</p>
                                            <time className="text-[9px] font-mono text-stone-400 uppercase tracking-widest mt-0.5 block">
                                                {entry.time}
                                            </time>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                </div>
  );
};

export default DeveloperOnboardingHub;
