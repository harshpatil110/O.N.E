import React, { useEffect, useState, useRef } from 'react';
import { X, MessageSquare, Bot, User, Loader2, AlertCircle, MessageSquareText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { getSessionChatHistory } from '../api/adminApi';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';

/**
 * ChatHistoryDrawer — Modified to utilize "Dark Enterprise" design system bindings
 */
export const ChatHistoryDrawer = ({ isOpen, onClose, sessionId, employeeName }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [totalMessages, setTotalMessages] = useState(0);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (!isOpen || !sessionId) return;

    const fetchHistory = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await getSessionChatHistory(sessionId);
        setMessages(data.messages || []);
        setTotalMessages(data.total_messages || 0);
      } catch (err) {
        console.error('Failed to fetch chat history:', err);
        setError('Unable to load conversation history. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [isOpen, sessionId]);

  // Scroll to bottom when messages load to see most recent
  useEffect(() => {
    if (scrollRef.current && messages.length > 0) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  const formatTimestamp = (ts) => {
    if (!ts) return '';
    try {
      // Append 'Z' to treat as UTC if the string doesn't specify timezone, then convert to local
      const dateString = ts.endsWith('Z') ? ts : ts + 'Z';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      });
    } catch {
      return '';
    }
  };

  return (
    <>
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop overlay */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-stone-900/40 z-40"
              onClick={onClose}
              aria-hidden="true"
            />

            {/* Drawer panel */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', bounce: 0, duration: 0.3 }}
              className="fixed top-0 right-0 h-full w-full sm:w-[540px] bg-[#F7F5F0] shadow-xl z-50 flex flex-col border-l border-stone-200 text-stone-900 font-sans"
              role="dialog"
              aria-modal="true"
              aria-label="Conversation History"
            >
        {/* ─── Header ─── */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-stone-200 bg-white">
            <div className="flex items-center gap-3">
                <div className="size-8 bg-stone-900 text-white flex items-center justify-center rounded-sm">
                    <MessageSquareText size={16} />
                </div>
                <div>
                <h2 className="text-base font-serif font-bold text-stone-900 tracking-tight">
                    Conversation Log
                </h2>
                <p className="text-[10px] font-mono font-bold uppercase tracking-widest text-stone-400">
                    {employeeName ? `User: ${employeeName}` : 'Session View'} • {totalMessages} messages
                </p>
                </div>
            </div>

            <button
                onClick={onClose}
                className="p-1.5 text-stone-500 hover:text-stone-900 bg-stone-100 rounded-sm border border-stone-200 hover:bg-stone-200 transition-colors"
                aria-label="Close drawer"
            >
                <X size={16} />
            </button>
        </div>

        {/* ─── Body ─── */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-6 space-y-6 bg-[#F7F5F0]">
          {/* Loading state */}
          {loading && (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-stone-500">
              <Loader2 className="w-6 h-6 animate-spin text-stone-900" />
              <span className="text-xs font-mono uppercase tracking-widest">Loading Conversation Stream...</span>
            </div>
          )}

          {/* Error state */}
          {!loading && error && (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-rose-800">
              <AlertCircle className="w-8 h-8 text-rose-700" />
              <span className="text-xs font-mono text-center">{error}</span>
              <button
                onClick={() => {
                  setError('');
                  setLoading(true);
                  getSessionChatHistory(sessionId)
                    .then(data => { setMessages(data.messages || []); setTotalMessages(data.total_messages || 0); })
                    .catch(() => setError('Database sync threshold failed. Please refresh.'))
                    .finally(() => setLoading(false));
                }}
                className="px-3 py-1.5 mt-2 bg-rose-50 border border-rose-200 rounded-sm text-xs font-mono font-bold uppercase tracking-wider text-rose-800 hover:bg-rose-100 transition-colors"
              >
                Attempt Re-Sync
              </button>
            </div>
          )}

          {/* Empty state */}
          {!loading && !error && messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-stone-400">
              <div className="size-12 rounded-sm bg-white flex items-center justify-center border border-stone-200 mb-1">
                 <MessageSquare className="w-6 h-6 text-stone-400" />
              </div>
              <span className="text-xs font-mono font-bold uppercase tracking-widest text-stone-500">No conversation history yet</span>
            </div>
          )}

          {/* Messages */}
          {!loading && !error && messages.length > 0 && (
            <div className="space-y-4 pb-4">
              {messages.map((msg, idx) => {
                const isUser = msg.role === 'user';
                return (
                  <div
                    key={idx}
                    className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
                  >
                    {/* Avatar */}
                    <div
                      className={`w-7 h-7 rounded-sm flex-shrink-0 flex items-center justify-center mt-1 text-xs font-mono font-bold border shadow-sm
                        ${isUser
                          ? 'bg-blue-200 text-blue-900 border-blue-300'
                          : 'bg-stone-900 text-white border-stone-900'
                        }`}
                    >
                      {isUser ? <User size={14} /> : 'O.'}
                    </div>

                    {/* Bubble */}
                    <div className={`flex flex-col max-w-[82%] ${isUser ? 'items-end' : 'items-start'}`}>
                      <span className="text-[9px] font-mono font-bold uppercase tracking-widest text-stone-400 mb-1 px-1">
                        {isUser ? 'User' : 'Assistant'}
                      </span>

                      <div
                        className={`px-4 py-3 rounded-md text-xs leading-relaxed border shadow-sm
                          ${isUser
                            ? 'bg-[#BFDBFE] text-stone-900 border-blue-300'
                            : 'bg-white text-stone-900 border-stone-200'
                          }`}
                      >
                        <div className="prose prose-xs max-w-none text-stone-900 prose-headings:font-serif prose-code:font-mono">
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      </div>

                      {/* Timestamp */}
                      {msg.timestamp && (
                        <span className="text-[9px] font-mono text-stone-400 mt-1 px-1 uppercase tracking-widest">
                          {formatTimestamp(msg.timestamp)}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* ─── Footer ─── */}
        <div className="px-6 py-3.5 border-t border-stone-200 bg-white flex justify-between items-center">
          <p className="text-[10px] font-mono text-stone-400 uppercase tracking-widest font-bold">
            Read-only conversation log
          </p>
          <p className="text-[10px] font-mono font-bold uppercase tracking-widest text-stone-700 bg-stone-100 px-2 py-0.5 rounded-sm border border-stone-200">
            {totalMessages} Messages
          </p>
        </div>
      </motion.div>
      </>
      )}
      </AnimatePresence>

      {/* Utilities */}
      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        
        /* Modal dark-themed custom scrollbars override */
        .custom-scrollbar::-webkit-scrollbar {
          width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #0B0B0E; 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #1e293b; 
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #334155; 
        }
      `}</style>
    </>
  );
};
