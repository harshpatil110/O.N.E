import React from 'react';

export const ProgressBar = ({ percentComplete, completedCount, totalCount }) => {
  const safePercent = Math.min(100, Math.max(0, percentComplete || 0));

  return (
    <div className="mb-6">
      <div className="flex justify-between items-center mb-2">
        <span className="text-xs font-semibold uppercase tracking-widest text-zinc-600">
          {completedCount || 0} of {totalCount || 0} tasks complete
        </span>
        <span className="text-xs font-bold text-zinc-800">{Math.round(safePercent)}%</span>
      </div>
      <div className="h-2 w-full border border-zinc-300 bg-white overflow-hidden relative">
        <div 
          className="absolute top-0 left-0 h-full bg-blue-600 transition-all duration-500 ease-out"
          style={{ width: `${safePercent}%` }}
        />
      </div>
    </div>
  );
};
