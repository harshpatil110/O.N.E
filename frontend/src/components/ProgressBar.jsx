import React from 'react';

export const ProgressBar = ({ percentComplete, completedCount, totalCount }) => {
  const safePercent = Math.min(100, Math.max(0, percentComplete || 0));

  return (
    <div className="mb-2">
      <div className="flex justify-between items-center mb-3">
        <span className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400">
          {completedCount || 0} / {totalCount || 0} completed
        </span>
        <span className="text-sm font-bold text-white">{Math.round(safePercent)}%</span>
      </div>
      <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden relative border border-white/5 shadow-inner">
        <div 
          className="absolute top-0 left-0 h-full bg-[#4c6ef5] transition-all duration-700 ease-out shadow-[0_0_10px_rgba(76,110,245,0.5)]"
          style={{ width: `${safePercent}%` }}
        />
      </div>
    </div>
  );
};
