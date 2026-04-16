import React from 'react';
import { CheckCircle2, Circle, Clock, FastForward } from 'lucide-react';

export const ChecklistItem = ({ item, onToggle }) => {
  const { id, title, status, category, required, completed_at } = item;

  const renderIcon = () => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 size={16} className={`flex-shrink-0 ${onToggle ? 'text-emerald-500 cursor-pointer hover:scale-110 transition-transform' : 'text-emerald-500'}`} />;
      case 'in_progress':
        return <Clock size={16} className={`flex-shrink-0 ${onToggle ? 'text-[#4c6ef5] cursor-pointer hover:scale-110 transition-transform' : 'text-[#4c6ef5]'}`} />;
      case 'skipped':
        return <FastForward size={16} className={`flex-shrink-0 ${onToggle ? 'text-amber-500 cursor-pointer hover:scale-110 transition-transform' : 'text-amber-500'}`} />;
      case 'pending':
      default:
        return <Circle size={16} className={`flex-shrink-0 ${onToggle ? 'text-slate-600 cursor-pointer hover:text-white transition-colors' : 'text-slate-600'}`} />;
    }
  };

  const isInProgress = status === 'in_progress';
  const isCompleted = status === 'completed';

  return (
    <div className={`p-4 rounded-xl border transition-all duration-300 group
      ${isInProgress ? 'bg-white/5 border-[#4c6ef5]/30 shadow-lg shadow-black/10' : 'bg-white/5 border-white/5'}
      ${onToggle ? 'hover:border-white/20' : ''}
    `}>
      <div className="flex items-start gap-3">
        <div 
          onClick={() => onToggle && onToggle(id, status)}
          className={`mt-0.5 ${onToggle ? 'cursor-pointer' : ''}`}
        >
          {renderIcon()}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
             <h4 className={`text-xs font-bold leading-relaxed truncate whitespace-normal
               ${isInProgress ? 'text-white' : 'text-slate-300'} 
               ${isCompleted ? 'line-through text-slate-500' : ''}`
             }>
               {title}
               {required && <span className="ml-1.5 inline-block w-1.5 h-1.5 bg-red-500/80 rounded-full shadow-[0_0_8px_rgba(239,68,68,0.5)] transform -translate-y-[2px]" title="Required"></span>}
             </h4>
          </div>
          
          <div className="mt-3 flex items-center justify-between">
            <span className="px-2 py-0.5 text-[9px] font-bold uppercase tracking-widest bg-white/5 border border-white/10 text-slate-400 rounded">
              {category || 'general'}
            </span>
            {isCompleted && completed_at && (
              <span className="text-[9px] text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1">
                <CheckCircle2 size={10} />
                Done
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
