import React from 'react';
import { CheckSquare, Square, PlaySquare, SkipForward } from 'lucide-react';

export const ChecklistItem = ({ item, onToggle }) => {
  const { id, title, status, category, required, completed_at } = item;

  const renderIcon = () => {
    switch (status) {
      case 'completed':
        return <CheckSquare className={`w-5 h-5 flex-shrink-0 ${onToggle ? 'text-slate-800 cursor-pointer hover:scale-110 transition-transform' : 'text-slate-500'}`} />;
      case 'in_progress':
        return <PlaySquare className={`w-5 h-5 flex-shrink-0 ${onToggle ? 'text-blue-700 cursor-pointer hover:scale-110 transition-transform' : 'text-blue-600'}`} />;
      case 'skipped':
        return <SkipForward className={`w-5 h-5 flex-shrink-0 ${onToggle ? 'text-yellow-700 cursor-pointer hover:scale-110 transition-transform' : 'text-yellow-600'}`} />;
      case 'pending':
      default:
        return <Square className={`w-5 h-5 flex-shrink-0 ${onToggle ? 'text-zinc-500 cursor-pointer hover:scale-110 transition-transform' : 'text-zinc-300'}`} />;
    }
  };

  const isInProgress = status === 'in_progress';
  const isCompleted = status === 'completed';

  return (
    <div className={`p-4 border border-zinc-200 bg-white mb-3 flex flex-col gap-2 transition-all duration-300 ${isInProgress ? 'border-l-4 border-l-blue-600 shadow-sm' : ''}`}>
      <div className="flex items-start gap-3">
        <div 
          onClick={() => onToggle && onToggle(id, status)}
          className={onToggle ? 'cursor-pointer' : ''}
        >
          {renderIcon()}
        </div>
        <div className="flex-1">
          <div className="flex items-start justify-between gap-2">
             <h4 className={`text-sm tracking-wide leading-snug ${isInProgress ? 'font-bold text-zinc-900' : 'font-medium text-zinc-700'} ${isCompleted ? 'line-through text-zinc-400' : ''}`}>
               {title}
               {required && <span className="ml-1.5 inline-block w-1.5 h-1.5 bg-red-600 transform -translate-y-1"></span>}
             </h4>
          </div>
          
          <div className="mt-3 flex items-center justify-between">
            <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest border border-zinc-200 text-zinc-500">
              {category || 'general'}
            </span>
            {isCompleted && completed_at && (
              <span className="text-[10px] text-zinc-400 font-medium uppercase tracking-wider">
                {new Date(completed_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

