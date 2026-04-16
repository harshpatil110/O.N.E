import React from 'react';
import { ProgressBar } from './ProgressBar';
import { ChecklistItem } from './ChecklistItem';
import { useChecklist } from '../context/ChecklistContext';
import { LayoutList, RefreshCw } from 'lucide-react';

export const ChecklistSidebar = () => {
  const { progress, loading, fetchProgress } = useChecklist();

  if (loading && (!progress || !progress.items || progress.items.length === 0)) {
    return (
      <div className="w-full h-full flex flex-col p-6 lg:p-8">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-white text-sm font-bold flex items-center gap-2">
            <LayoutList size={18} className="text-[#4c6ef5]" />
            Onboarding Plan
          </h3>
        </div>
        <div className="flex-1 flex items-center justify-center animate-pulse text-center text-slate-500 text-xs font-bold uppercase tracking-widest">
           Initializing variables...
        </div>
      </div>
    );
  }

  if (!progress || !progress.items || progress.items.length === 0) {
    return (
      <div className="w-full h-full flex flex-col p-6 lg:p-8">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-white text-sm font-bold flex items-center gap-2">
            <LayoutList size={18} className="text-[#4c6ef5]" />
            Onboarding Plan
          </h3>
        </div>
        <div className="flex-1 flex flex-col items-center justify-center text-center text-slate-400">
          <div className="size-12 bg-white/5 border border-white/10 flex items-center justify-center rounded-xl mb-4 text-[#4c6ef5]">
             <LayoutList size={20} />
          </div>
          <p className="text-sm font-bold text-white mb-2">Awaiting Variables</p>
          <p className="text-xs text-slate-500 max-w-[200px] leading-relaxed">
            Please complete the initial profiling with O.N.E. to map your tailored onboarding sequence.
          </p>
        </div>
      </div>
    );
  }

  const { percent_complete, completed_count, items } = progress;
  const total_count = items.length;

  const groups = items.reduce((acc, item) => {
    const cat = item.category || 'general';
    if (!acc[cat]) {
      acc[cat] = [];
    }
    acc[cat].push(item);
    return acc;
  }, {});

  return (
    <div className="w-full h-full flex flex-col p-6 lg:p-8">
      <div className="flex items-center justify-between mb-8">
        <h3 className="text-white text-sm font-bold flex items-center gap-2">
          <LayoutList size={18} className="text-[#4c6ef5]" />
          Onboarding Plan
        </h3>
        <button 
          className={`p-1.5 text-slate-500 hover:text-white transition-colors rounded-lg hover:bg-white/5 ${loading ? 'animate-spin text-[#4c6ef5]' : ''}`}
          onClick={() => fetchProgress()}
          title="Sync Progress"
        >
          <RefreshCw size={14} />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
        <ProgressBar 
          percentComplete={percent_complete || 0} 
          completedCount={completed_count || 0} 
          totalCount={total_count} 
        />
        
        <div className="space-y-8 mt-10">
          {Object.entries(groups).map(([category, catItems]) => {
            const catCompleted = catItems.filter(i => i.status === 'completed' || i.status === 'skipped').length;
            const catTotal = catItems.length;
            
            return (
              <div key={category}>
                <div className="flex items-center justify-between mb-4 border-b border-[#1f1f23] pb-2">
                  <h4 className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-500">
                    {category}
                  </h4>
                  <span className="text-[10px] font-bold text-slate-500 bg-white/5 px-2 py-0.5 rounded-full border border-white/5">
                    {catCompleted}/{catTotal}
                  </span>
                </div>
                
                <div className="space-y-3">
                  {catItems.map((item, idx) => (
                    <ChecklistItem key={item.id || idx} item={item} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #1f1f23; border-radius: 4px; }
        .custom-scrollbar:hover::-webkit-scrollbar-thumb { background: #333; }
      `}} />
    </div>
  );
};
