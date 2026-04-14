import React from 'react';
import { ProgressBar } from './ProgressBar';
import { ChecklistItem } from './ChecklistItem';
import { useChecklist } from '../context/ChecklistContext';

export const ChecklistSidebar = () => {
  const { progress, loading } = useChecklist();

  if (loading) {
    return (
      <div className="w-[30%] flex-shrink-0 flex flex-col bg-[#F7F5F0] border-l border-zinc-300">
        <div className="h-16 px-8 flex items-center border-b border-zinc-200">
          <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-500">Progress Tracker</h3>
        </div>
        <div className="flex-1 flex items-center justify-center p-8 animate-pulse text-center text-zinc-400 text-xs">
           Initializing checklist...
        </div>
      </div>
    );
  }

  if (!progress || !progress.items || progress.items.length === 0) {
    return (
      <div className="w-[30%] flex-shrink-0 flex flex-col bg-[#F7F5F0] border-l border-zinc-300">
        <div className="h-16 px-8 flex items-center border-b border-zinc-200 bg-white">
          <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-800">Progress Tracker</h3>
        </div>
        <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-zinc-500 text-xs">
          <svg className="w-12 h-12 mb-4 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M5 13l4 4L19 7" />
          </svg>
          <p className="text-sm font-semibold text-zinc-600 mb-1">All caught up!</p>
          <p>No tasks assigned yet.</p>
        </div>
      </div>
    );
  }

  const { percent_complete, completed_count, items } = progress;
  const total_count = items.length;

  // Group items by category
  const groups = items.reduce((acc, item) => {
    const cat = item.category || 'general';
    if (!acc[cat]) {
      acc[cat] = [];
    }
    acc[cat].push(item);
    return acc;
  }, {});

  return (
    <div className="w-[30%] flex-shrink-0 flex flex-col bg-[#F7F5F0] border-l border-zinc-300">
      <div className="h-16 px-8 flex items-center border-b border-zinc-200 bg-white">
        <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-800">Progress Tracker</h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 md:p-8">
        <ProgressBar 
          percentComplete={percent_complete || 0} 
          completedCount={completed_count || 0} 
          totalCount={total_count} 
        />
        
        <div className="space-y-8 mt-8">
          {Object.entries(groups).map(([category, catItems]) => {
            const catCompleted = catItems.filter(i => i.status === 'completed' || i.status === 'skipped').length;
            const catTotal = catItems.length;
            
            return (
              <div key={category}>
                <div className="flex items-center justify-between mb-4 border-b border-zinc-200 pb-2">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-900">
                    {category}
                  </h4>
                  <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-500">
                    ({catCompleted}/{catTotal})
                  </span>
                </div>
                
                <div>
                  {catItems.map((item, idx) => (
                    <ChecklistItem key={item.id || idx} item={item} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
