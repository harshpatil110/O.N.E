import React from 'react';
import { Database, Book, FileText, Share2, Users2, Activity, PlaySquare, Check, CheckSquare } from 'lucide-react';
import { useChecklist } from '../context/ChecklistContext';
import { updateChecklistItem } from '../api/checklist';

export const ContextualSidebar = () => {
  const { progress, fetchProgress } = useChecklist();

  const toggleTask = async (task) => {
    if (task.status === 'completed') return; 
    try {
      await updateChecklistItem(task.id, 'completed');
      fetchProgress(); // Re-sync context
    } catch (e) {
      console.error("Failed to mark task as done", e);
    }
  };

  const dummyTasks = [
    { id: 'dummy-1', title: 'Configure local development environment', status: 'completed' },
    { id: 'dummy-2', title: 'Review Core Architecture ADRs', status: 'pending' },
    { id: 'dummy-3', title: 'Set up staging DB credentials', status: 'pending' },
    { id: 'dummy-4', title: 'Join #engineering Slack channel', status: 'pending' }
  ];

  const activeItems = progress?.items?.length > 0 ? progress.items : dummyTasks;
  const pendingTasks = activeItems.filter(t => t.status !== 'completed');
  const completedTasks = activeItems.filter(t => t.status === 'completed');

  return (
    <div className="w-full h-full flex flex-col p-6 lg:p-8 bg-[#111114] overflow-y-auto scrollbar-hide">
      <h3 className="text-white text-sm font-bold mb-8 flex items-center gap-2">
        <CheckSquare size={16} className="text-[#4c6ef5]" /> Action & Context
      </h3>
      
      <div className="space-y-10 pb-10">
        
        {/* Pending Tasks */}
        <div className="space-y-4">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.15em]">Pending Tasks</p>
          <div className="bg-white/5 border border-white/10 rounded-xl overflow-hidden shadow-sm min-h-[60px] flex flex-col justify-center">
            {pendingTasks.length > 0 ? (
              pendingTasks.map((task) => (
                <div key={task.id} className="p-4 flex items-start gap-4 hover:bg-white/[0.02] transition-colors border-b border-white/5 last:border-0 group cursor-pointer" onClick={() => toggleTask(task)}>
                  <div className="flex-shrink-0 mt-0.5">
                      <div className="size-4 border-2 border-slate-600 rounded flex items-center justify-center group-hover:border-[#4c6ef5] transition-colors" />
                  </div>
                  <div className="flex-1 min-w-0">
                      <h6 className="text-xs font-bold text-slate-300 tracking-tight leading-tight group-hover:text-white transition-colors">{task.title}</h6>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-4 text-center">
                <p className="text-xs font-bold text-slate-500 tracking-tight">O.N.E. is evaluating your profile...</p>
                <p className="text-[10px] text-slate-600 mt-1 uppercase tracking-widest">Tasks will appear here shortly</p>
              </div>
            )}
          </div>
        </div>

        {/* Completed Tasks */}
        {(completedTasks.length > 0 || pendingTasks.length > 0) && (
          <div className="space-y-4">
            <p className="text-[10px] font-bold text-emerald-500/50 uppercase tracking-[0.15em]">Completed Tasks</p>
            {completedTasks.length > 0 ? (
              <div className="space-y-2">
                {completedTasks.map((task) => (
                  <div key={task.id} className="p-3 flex items-center gap-3 bg-emerald-500/5 border border-emerald-500/10 rounded-lg">
                      <Check size={14} className="text-emerald-500 opacity-80" />
                      <h6 className="text-xs font-semibold text-slate-500 line-through tracking-tight">{task.title}</h6>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-3 bg-white/5 border border-white/10 rounded-lg text-center">
                <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">No tasks completed yet</p>
              </div>
            )}
          </div>
        )}

        {/* Active Repository Card */}
        <div className="space-y-4">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.15em]">Active Repository</p>
          <div className="bg-[#0a0a0c] p-5 rounded-xl border border-white/10 shadow-sm hover:border-[#4c6ef5]/30 transition-colors cursor-default">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-[#4c6ef5]/10 text-[#4c6ef5]">
                <Database size={16} />
              </div>
              <span className="text-sm font-bold text-white">auth-service</span>
            </div>
            <p className="text-[11px] text-slate-400 mb-5 leading-relaxed font-medium">Core authentication and identity provider service.</p>
            <div className="flex items-center gap-4 border-t border-white/5 pt-4">
              <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-500">
                <Activity size={12} />
                2H AGO
              </div>
              <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-500">
                <Share2 size={12} />
                A4F8E2
              </div>
            </div>
          </div>
        </div>

        {/* Useful Links */}
        <div className="space-y-4">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.15em]">Useful Links</p>
          <ul className="space-y-2 text-sm">
            <li>
              <a className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 group transition-colors border border-transparent hover:border-white/10" href="#">
                <div className="flex items-center gap-3">
                  <Book size={16} className="text-slate-500 group-hover:text-[#4c6ef5] transition-colors" />
                  <span className="text-xs text-slate-400 group-hover:text-white font-bold transition-colors">Internal API Docs</span>
                </div>
                <PlaySquare size={14} className="text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity" />
              </a>
            </li>
            <li>
              <a className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 group transition-colors border border-transparent hover:border-white/10" href="#">
                <div className="flex items-center gap-3">
                  <FileText size={16} className="text-slate-500 group-hover:text-[#4c6ef5] transition-colors" />
                  <span className="text-xs text-slate-400 group-hover:text-white font-bold transition-colors">Architecture ADRs</span>
                </div>
                <PlaySquare size={14} className="text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity" />
              </a>
            </li>
            <li>
              <a className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 group transition-colors border border-transparent hover:border-white/10" href="#">
                <div className="flex items-center gap-3">
                  <Share2 size={16} className="text-slate-500 group-hover:text-[#4c6ef5] transition-colors" />
                  <span className="text-xs text-slate-400 group-hover:text-white font-bold transition-colors">Deployment Topology</span>
                </div>
                <PlaySquare size={14} className="text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity" />
              </a>
            </li>
          </ul>
        </div>

        {/* Team Availability */}
        <div className="space-y-4">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.15em]">Team Availability</p>
          <div className="flex -space-x-2 overflow-hidden mb-4">
            <div className="size-8 rounded-full bg-indigo-500/20 ring-2 ring-[#111114] flex items-center justify-center text-indigo-400 font-bold text-xs">AJ</div>
            <div className="size-8 rounded-full bg-emerald-500/20 ring-2 ring-[#111114] flex items-center justify-center text-emerald-400 font-bold text-xs">SM</div>
            <div className="size-8 rounded-full bg-rose-500/20 ring-2 ring-[#111114] flex items-center justify-center text-rose-400 font-bold text-xs">KT</div>
            <div className="size-8 rounded-full bg-white/10 flex items-center justify-center ring-2 ring-[#111114] text-[10px] text-slate-400 font-bold">+2</div>
          </div>
          <p className="text-xs text-slate-400 font-medium leading-relaxed">
            Alex and Jordan are online to answer repository-specific questions.
          </p>
        </div>

      </div>
    </div>
  );
};
