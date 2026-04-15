import React, { useEffect, useState, useRef } from 'react';
import { X, MessageSquare, Bot, User, Loader2, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { getSessionChatHistory } from '../api/adminApi';

/**
 * ChatHistoryDrawer — A slide-over drawer that displays the full audit trail
 * of the conversation between an employee and the O.N.E. chatbot.
 * Matches the "Warm Editorial Minimalism" design system used across the admin UI.
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

  // Scroll to top when messages load
  useEffect(() => {
    if (scrollRef.current && messages.length > 0) {
      scrollRef.current.scrollTop = 0;
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
      const date = new Date(ts);
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
      {/* Backdrop overlay */}
      <div
        className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 transition-opacity duration-300"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer panel */}
      <div
        className="fixed top-0 right-0 h-full w-full sm:w-[520px] bg-[#F7F5F0] shadow-2xl z-50 flex flex-col
                   transform transition-transform duration-300 ease-out"
        role="dialog"
        aria-modal="true"
        aria-label="Conversation History"
      >
        {/* ─── Header ─── */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-[#EAE8E2] bg-white">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-slate-800 text-white flex items-center justify-center flex-shrink-0">
              <MessageSquare size={18} />
            </div>
            <div>
              <h2 className="text-base font-semibold text-slate-900 tracking-tight leading-tight">
                Conversation Log
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                {employeeName ? `${employeeName}` : 'Session'} · {totalMessages} messages
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition-colors"
            aria-label="Close drawer"
          >
            <X size={20} />
          </button>
        </div>

        {/* ─── Body ─── */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-6 space-y-1">
          {/* Loading state */}
          {loading && (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-slate-400">
              <Loader2 className="w-8 h-8 animate-spin" />
              <span className="text-sm font-medium uppercase tracking-widest">Loading history…</span>
            </div>
          )}

          {/* Error state */}
          {!loading && error && (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-red-500">
              <AlertCircle className="w-8 h-8" />
              <span className="text-sm text-center">{error}</span>
              <button
                onClick={() => {
                  setError('');
                  setLoading(true);
                  getSessionChatHistory(sessionId)
                    .then(data => { setMessages(data.messages || []); setTotalMessages(data.total_messages || 0); })
                    .catch(() => setError('Still unable to load. Please try again later.'))
                    .finally(() => setLoading(false));
                }}
                className="text-xs font-semibold uppercase tracking-wider text-slate-700 underline hover:text-slate-900"
              >
                Retry
              </button>
            </div>
          )}

          {/* Empty state */}
          {!loading && !error && messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-slate-400">
              <MessageSquare className="w-10 h-10" />
              <span className="text-sm font-medium uppercase tracking-widest">No messages yet</span>
              <span className="text-xs text-slate-400">The conversation history will appear here once the employee starts chatting.</span>
            </div>
          )}

          {/* Messages */}
          {!loading && !error && messages.length > 0 && (
            <div className="space-y-4">
              {messages.map((msg, idx) => {
                const isUser = msg.role === 'user';
                return (
                  <div
                    key={idx}
                    className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} animate-fade-in`}
                    style={{ animationDelay: `${Math.min(idx * 30, 300)}ms` }}
                  >
                    {/* Avatar */}
                    <div
                      className={`w-8 h-8 flex-shrink-0 flex items-center justify-center mt-1
                        ${isUser
                          ? 'bg-blue-500 text-white'
                          : 'bg-slate-800 text-white'
                        }`}
                    >
                      {isUser ? <User size={14} /> : <Bot size={14} />}
                    </div>

                    {/* Bubble */}
                    <div className={`flex flex-col max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
                      {/* Role label */}
                      <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1 px-1">
                        {isUser ? 'Employee' : 'O.N.E.'}
                      </span>

                      <div
                        className={`px-4 py-3 border text-sm leading-relaxed
                          ${isUser
                            ? 'bg-blue-500 text-white border-blue-500'
                            : 'bg-white text-slate-800 border-[#EAE8E2]'
                          }`}
                      >
                        <div className={`prose prose-sm max-w-none ${isUser ? 'prose-invert' : ''}`}>
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      </div>

                      {/* Timestamp */}
                      {msg.timestamp && (
                        <span className="text-[10px] text-slate-400 mt-1 px-1 font-medium">
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
        <div className="px-6 py-3 border-t border-[#EAE8E2] bg-white">
          <p className="text-[10px] text-slate-400 uppercase tracking-widest text-center font-medium">
            Read-only audit trail · {totalMessages} total messages
          </p>
        </div>
      </div>

      {/* Fade-in animation keyframe (injected once) */}
      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out both;
        }
      `}</style>
    </>
  );
};
