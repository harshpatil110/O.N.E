import React, { useEffect, useState } from 'react';
import { ProgressBar } from './ProgressBar';
import { ChecklistItem } from './ChecklistItem';
import { getProgress } from '../api/checklist';

export const ChecklistSidebar = ({ sessionId }) => {
  const [progressData, setProgressData] = useState(null);

  useEffect(() => {
    if (!sessionId) return;
    
    let isMounted = true;
    let intervalId = null;

    const fetchProgress = async () => {
      try {
        const data = await getProgress(sessionId);
        if (isMounted) {
          setProgressData(data);
          if (data.session_status === 'completed' && intervalId) {
            clearInterval(intervalId);
          }
        }
      } catch (err) {
        console.error("Failed to fetch progress", err);
      }
    };

    // Initial fetch
    fetchProgress();

    // Poll every 3 seconds
    intervalId = setInterval(fetchProgress, 3000);

    return () => {
      isMounted = false;
      if (intervalId) clearInterval(intervalId);
    };
  }, [sessionId]);

  if (!progressData) {
    return (
      <div className="w-[30%] flex-shrink-0 flex flex-col bg-[#F7F5F0] border-l border-zinc-300">
        <div className="h-16 px-8 flex items-center border-b border-zinc-200">
          <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-500">Progress Tracker</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-8 animate-pulse">
           <div className="h-6 bg-zinc-200 w-full mb-6 relative"></div>
           <div className="h-24 bg-white border border-zinc-200 mb-3"></div>
           <div className="h-24 bg-white border border-zinc-200 mb-3"></div>
        </div>
      </div>
    );
  }

  const { percent_complete, completed_count, items } = progressData;
  const total_count = items?.length || 0;

  // Group items by category
  const groups = items?.reduce((acc, item) => {
    const cat = item.category || 'general';
    if (!acc[cat]) {
      acc[cat] = [];
    }
    acc[cat].push(item);
    return acc;
  }, {}) || {};

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
