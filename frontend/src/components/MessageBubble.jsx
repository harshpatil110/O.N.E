import React from 'react';
import ReactMarkdown from 'react-markdown';

export const MessageBubble = ({ role, content, isLoadingIndicator = false }) => {
  const isUser = role === 'user';

  // Warm Editorial Minimalism constraints applied here
  const baseClasses = 'max-w-[85%] px-6 py-4 border border-zinc-200 shadow-sm md:max-w-[70%]';
  const roleClasses = isUser
    ? 'ml-auto bg-blue-500 text-white rounded-none border-blue-500'
    : 'mr-auto bg-gray-100 text-gray-900 rounded-none border-gray-100';

  if (isLoadingIndicator) {
    return (
      <div className={`${baseClasses} ${roleClasses} flex items-center space-x-1.5 min-w-[80px]`}>
        <div className="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
    );
  }

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} items-end space-x-2`}>
      {!isUser && (
        <div className="w-8 h-8 flex-shrink-0 bg-zinc-800 text-white flex items-center justify-center text-[10px] font-bold tracking-tighter">
          ONE
        </div>
      )}
      <div className={`${baseClasses} ${roleClasses}`}>
        <div className={`prose prose-sm max-w-none ${isUser ? 'prose-invert' : ''}`}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};
