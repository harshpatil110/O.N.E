import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Bot, Zap } from 'lucide-react';

export const MessageBubble = ({ role, content, metadata, isLoadingIndicator = false }) => {
  const isUser = role === 'user';

  // Detect if external workspace context was used (via Hermes delegation or metadata)
  const isExternalWorkspace = Boolean(
    metadata?.external_workspace ||
    metadata?.source === 'hermes' ||
    (typeof content === 'string' && (
      content.includes('⚡ ROUTING TO HERMES') ||
      content.includes('[HERMES]') ||
      content.includes('Hermes Agent') ||
      content.includes('hermes gateway') ||
      content.toLowerCase().includes('connected tools: slack, notion, vercel, jira, confluence')
    ))
  );

  const baseClasses = 'max-w-[85%] px-5 py-3.5 md:max-w-[75%] leading-relaxed text-[14px] font-sans';
  
  // Warm Editorial Minimalism bubble styling
  const roleClasses = isUser
    ? 'ml-auto bg-[#BFDBFE] text-stone-900 border border-blue-300/60 rounded-md rounded-tr-none shadow-sm'
    : 'mr-auto bg-white text-stone-900 border border-stone-200/80 rounded-md rounded-tl-none shadow-sm';

  if (isLoadingIndicator) {
    return (
      <div className={`flex w-full justify-start items-end space-x-3`}>
        <div className="w-7 h-7 flex-shrink-0 bg-stone-900 text-stone-100 rounded-sm flex items-center justify-center shadow-sm">
          <Bot size={14} />
        </div>
        <div className={`${baseClasses} ${roleClasses} flex items-center space-x-1.5 h-[40px] px-4`}>
          <div className="w-1.5 h-1.5 bg-stone-400 rounded-full animate-pulse flex-shrink-0" style={{ animationDelay: '0ms' }} />
          <div className="w-1.5 h-1.5 bg-stone-400 rounded-full animate-pulse flex-shrink-0" style={{ animationDelay: '150ms' }} />
          <div className="w-1.5 h-1.5 bg-stone-400 rounded-full animate-pulse flex-shrink-0" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    );
  }

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} items-end space-x-3 group`}>
      {!isUser && (
        <div className="w-7 h-7 flex-shrink-0 bg-stone-900 text-stone-100 rounded-sm flex items-center justify-center shadow-sm">
          <Bot size={14} />
        </div>
      )}
      <div className={`${baseClasses} ${roleClasses}`}>
        {!isUser && isExternalWorkspace && (
          <div className="inline-flex items-center gap-1.5 px-2 py-0.5 mb-2.5 text-[10px] font-mono tracking-wider text-amber-800 bg-amber-50/90 border border-amber-200/80 rounded select-none shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
            <Zap size={11} className="text-amber-600 fill-amber-500/20 flex-shrink-0" />
            <span className="font-semibold uppercase tracking-wider">Workspace Context (Hermes)</span>
          </div>
        )}
        <div className={`prose prose-sm max-w-none ${isUser ? 'text-stone-900 prose-strong:text-stone-900' : 'text-stone-800 prose-headings:font-serif prose-a:text-blue-700 prose-strong:text-stone-900 prose-code:font-mono prose-code:bg-stone-100 prose-code:text-stone-800 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-sm'}`}>
          <ReactMarkdown>{typeof content === 'string' && content.length > 0 ? content : '*⚠️ EMPTY — No content string received*'}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};
