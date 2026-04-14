import React, { useState, useRef, useEffect } from 'react';
import { useChecklist } from '../context/ChecklistContext';

export const ChatInput = ({ onSendMessage, disabled }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const { markCurrentTaskDone, loading: isActionLoading } = useChecklist();

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      // Restrict max-height approximation for ~4 lines (approx 96px depending on line-height)
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [text]);

  const handleSubmit = () => {
    if (text.trim() && !disabled) {
      onSendMessage(text.trim());
      setText('');
      // Reset height
      if (textareaRef.current) textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const quickActions = [
    { label: 'Mark as done', action: markCurrentTaskDone },
    { label: 'Ask for help', fill: 'Can you explain this in more detail?' },
    { label: 'Skip this', fill: 'Can I skip this task?' }
  ];

  const handleQuickAction = (actionLabel, action, fillContent) => {
    if (disabled || isActionLoading) return;
    
    if (actionLabel === 'Ask for help' || actionLabel === 'Skip this') {
      console.log(`Action triggered: ${actionLabel}`);
      // Send the message immediately for better demo experience
      if (fillContent) {
        onSendMessage(fillContent);
      }
      return;
    }

    if (action) {
      console.log(`Action triggered: ${actionLabel}`);
      action();
    } else if (fillContent) {
      setText(fillContent);
      if (textareaRef.current) textareaRef.current.focus();
    }
  };

  return (
    <div className="w-full flex flex-col space-y-3 pt-4 border-t border-zinc-200">
      <div className="flex gap-2 text-xs">
        {quickActions.map((action, idx) => (
          <button
            key={idx}
            onClick={() => handleQuickAction(action.label, action.action, action.fill)}
            className="px-3 py-1.5 border border-zinc-300 text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 transition-colors uppercase tracking-wider text-[10px] font-medium"
            disabled={disabled || isActionLoading}
          >
            {action.label}
          </button>
        ))}
      </div>
      
      <div className="flex items-end space-x-3">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={disabled}
          className="flex-1 resize-none overflow-y-auto px-4 py-3 border border-zinc-300 bg-white text-zinc-800 placeholder-zinc-400 focus:outline-none focus:border-zinc-800 transition-colors shadow-sm"
          rows={1}
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !text.trim()}
          className="h-[46px] px-8 bg-zinc-900 text-white font-medium hover:bg-zinc-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors tracking-wide uppercase text-xs"
        >
          Send
        </button>
      </div>
    </div>
  );
};
