import React, { useEffect, useState, useRef } from 'react';
import { X, MessageSquare, Bot, User, Loader2, AlertCircle, MessageSquareText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { getSessionChatHistory } from '../api/adminApi';

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

  if (!isOpen) return null;

  return (
    <>
      {/* Dark Enterprise Backdrop overlay */}
      <div
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40 transition-opacity duration-300"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer panel */}
      <div
        className="fixed top-0 right-0 h-full w-full sm:w-[560px] bg-[#0B0B0E] shadow-2xl shadow-black/50 z-50 flex flex-col transform transition-transform duration-300 ease-out border-l border-white/5"
        role="dialog"
        aria-modal="true"
        aria-label="Conversation History"
      >
        {/* ─── Header ─── */}
        <div className="flex items-center justify-between px-8 py-6 border-b border-white/5 bg-[#13131A] relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-indigo-500 to-emerald-400" />
            <div className="flex items-center gap-4 relative z-10">
                <div className="size-10 bg-indigo-500/10 text-indigo-400 flex items-center justify-center rounded-xl border border-indigo-500/20">
                    <MessageSquareText size={20} />
                </div>
                <div>
                <h2 className="text-lg font-bold text-white tracking-tight leading-tight">
                    Conversation Log
                </h2>
                <p className="text-[11px] font-bold uppercase tracking-widest text-slate-500 mt-1">
                    {employeeName ? `User: ${employeeName}` : 'Session View'} <span className="text-slate-600 mx-1">•</span> {totalMessages} messages
                </p>
                </div>
            </div>

            <button
                onClick={onClose}
                className="p-2 text-slate-500 hover:text-white bg-[#0B0B0E] rounded-lg border border-white/5 hover:border-slate-700 transition-all z-10"
                aria-label="Close drawer"
            >
                <X size={18} />
            </button>
        </div>

        {/* ─── Body ─── */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto px-8 py-8 space-y-6 custom-scrollbar bg-[#0B0B0E]">
          {/* Loading state */}
          {loading && (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-indigo-400">
              <Loader2 className="w-8 h-8 animate-spin" />
              <span className="text-xs font-bold uppercase tracking-widest animate-pulse">Decrypting Event Stream...</span>
            </div>
          )}

          {/* Error state */}
          {!loading && error && (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-rose-400">
              <AlertCircle className="w-10 h-10 text-rose-500" />
              <span className="text-sm font-medium text-center">{error}</span>
              <button
                onClick={() => {
                  setError('');
                  setLoading(true);
                  getSessionChatHistory(sessionId)
                    .then(data => { setMessages(data.messages || []); setTotalMessages(data.total_messages || 0); })
                    .catch(() => setError('Database sync threshold failed. Please refresh the diagnostic pane.'))
                    .finally(() => setLoading(false));
                }}
                className="px-4 py-2 mt-2 bg-rose-500/10 border border-rose-500/20 rounded-lg text-xs font-bold uppercase tracking-wider text-rose-300 hover:bg-rose-500/20 hover:text-rose-200 transition-all"
              >
                Attempt Re-Sync
              </button>
            </div>
          )}

          {/* Empty state */}
          {!loading && !error && messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-slate-500">
              <div className="size-16 rounded-full bg-white/5 flex items-center justify-center border border-white/10 mb-2">
                 <MessageSquare className="w-8 h-8 text-slate-600" />
              </div>
              <span className="text-sm font-bold uppercase tracking-widest text-slate-400">No conversation history yet</span>
              <span className="text-xs text-slate-600 font-medium">The neural interface is standing by for initialization.</span>
            </div>
          )}

          {/* Messages */}
          {!loading && !error && messages.length > 0 && (
            <div className="space-y-6 pb-4">
              {messages.map((msg, idx) => {
                const isUser = msg.role === 'user';
                return (
                  <div
                    key={idx}
                    className={`flex gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'} animate-fade-in`}
                    style={{ animationDelay: `${Math.min(idx * 30, 300)}ms` }}
                  >
                    {/* Avatar */}
                    <div
                      className={`w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center mt-1 border shadow-sm
                        ${isUser
                          ? 'bg-slate-800 text-slate-300 border-white/10'
                          : 'bg-indigo-500 text-white border-indigo-400 shadow-indigo-500/20'
                        }`}
                    >
                      {isUser ? <User size={18} /> : 
                       <div className="font-black text-[10px] tracking-tighter flex items-center">
                            O.N.E.
                       </div>
                      }
                    </div>

                    {/* Bubble */}
                    <div className={`flex flex-col max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
                      {/* Role label */}
                      <span className="text-[10px] font-bold uppercase tracking-widest mb-1.5 px-1 shadow-sm">
                        {isUser ? (
                             <span className="text-slate-500">Subject Log</span>
                        ) : (
                             <span className="text-indigo-400">System Broadcast</span>
                        )}
                      </span>

                      <div
                        className={`px-5 py-4 rounded-2xl text-sm leading-relaxed border
                          ${isUser
                            ? 'bg-slate-800 text-slate-200 border-slate-700 rounded-tr-sm'
                            : 'bg-indigo-500/10 text-indigo-100 border-indigo-500/20 rounded-tl-sm'
                          }`}
                      >
                        <div className="prose prose-sm prose-invert max-w-none text-opacity-90">
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      </div>

                      {/* Timestamp */}
                      {msg.timestamp && (
                        <span className="text-[10px] text-slate-500 mt-2 px-1 font-bold tracking-wider uppercase">
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
        <div className="px-8 py-4 border-t border-white/5 bg-[#13131A] flex justify-between items-center">
          <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">
            Read-only deployment stream
          </p>
          <p className="text-[10px] text-indigo-400 uppercase tracking-widest font-bold bg-indigo-500/10 px-2 py-1 rounded border border-indigo-500/20">
            {totalMessages} Total Packets
          </p>
        </div>
      </div>

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
