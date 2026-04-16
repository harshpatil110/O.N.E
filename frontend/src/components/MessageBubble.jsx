import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Bot } from 'lucide-react';

export const MessageBubble = ({ role, content, isLoadingIndicator = false }) => {
  const isUser = role === 'user';

  const baseClasses = 'max-w-[85%] px-5 py-3.5 md:max-w-[75%] leading-relaxed text-[14px]';
  
  // Dark UI styling based on Stitch design
  const roleClasses = isUser
    ? 'ml-auto bg-[#4c6ef5] text-white rounded-2xl rounded-tr-sm shadow-lg shadow-[#4c6ef5]/20'
    : 'mr-auto bg-[#111114] text-slate-300 rounded-2xl rounded-tl-sm border border-[#1f1f23] shadow-lg shadow-black/20';

  if (isLoadingIndicator) {
    return (
      <div className={`flex w-full justify-start items-end space-x-3`}>
        <div className="w-8 h-8 flex-shrink-0 bg-white/5 border border-white/10 rounded-lg flex items-center justify-center text-[#4c6ef5]">
          <Bot size={16} />
        </div>
        <div className={`${baseClasses} ${roleClasses} flex items-center space-x-1.5 h-[42px] px-5`}>
          <div className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-pulse flex-shrink-0" style={{ animationDelay: '0ms' }} />
          <div className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-pulse flex-shrink-0" style={{ animationDelay: '150ms' }} />
          <div className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-pulse flex-shrink-0" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    );
  }

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} items-end space-x-3 group`}>
      {!isUser && (
        <div className="w-8 h-8 flex-shrink-0 bg-white/5 border border-white/10 rounded-lg flex items-center justify-center text-[#4c6ef5] shadow-sm">
          <Bot size={16} />
        </div>
      )}
      <div className={`${baseClasses} ${roleClasses}`}>
        <div className={`prose prose-sm max-w-none ${isUser ? 'prose-invert text-white' : 'prose-invert text-slate-300 prose-a:text-[#4c6ef5] prose-strong:text-white prose-code:text-emerald-400 prose-code:bg-emerald-400/10 prose-code:px-1 prose-code:rounded'}`}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};
