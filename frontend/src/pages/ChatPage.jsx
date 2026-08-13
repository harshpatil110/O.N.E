import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useChat } from '../hooks/useChat';
import { startSession } from '../api/chat';
import { MessageBubble } from '../components/MessageBubble';
import { ChatInput } from '../components/ChatInput';
import { ChecklistProvider, useChecklist } from '../context/ChecklistContext';

const ChatPageInner = ({ sessionId, setSessionId }) => {
  const [initError, setInitError] = useState(null);
  const endOfMessagesRef = useRef(null);
  const { fetchProgress } = useChecklist();

  const handleMessageComplete = useCallback(() => {
    setTimeout(() => {
      fetchProgress();
    }, 300);
  }, [fetchProgress]);

  const { messages, isLoading, sendMessage, appendInitialMessage, loadHistory } = useChat(sessionId, handleMessageComplete);

  useEffect(() => {
    const initializeSession = async () => {
      try {
        const data = await startSession();
        const sid = data.session_id;
        setSessionId(sid);
        const history = await loadHistory(sid);
        if (data.message && (!history || history.length === 0)) {
            appendInitialMessage(data.message);
        }
      } catch (err) {
        setInitError("Failed to initialize session. Please refresh.");
        console.error(err);
      }
    };
    initializeSession();
  }, [appendInitialMessage, loadHistory, setSessionId]);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex h-screen bg-[#0a0a0c] text-slate-300 overflow-hidden font-sans selection:bg-[#4c6ef5]/30">
      
      {/* Background Pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40 mix-blend-screen"
        style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0)',
          backgroundSize: '24px 24px'
        }}
      />

      {/* LEFT PANEL: Chat Interface */}
      <div className="relative flex flex-col z-10 transition-all duration-300 ease-in-out w-full">
        
        {/* Header */}
        <div className="h-16 px-6 lg:px-12 flex items-center border-b border-[#1f1f23] bg-transparent backdrop-blur-md">
          <div className="flex items-center gap-2.5">
            <div className="size-7 bg-[#4c6ef5] rounded flex items-center justify-center text-white shadow-lg shadow-[#4c6ef5]/20">
              <span className="font-bold font-mono text-sm tracking-tighter">O.</span>
            </div>
            <h2 className="text-white text-lg font-extrabold tracking-tight">O.N.E</h2>
          </div>

          <div className="ml-auto flex items-center space-x-6">
            <div className="hidden md:flex items-center gap-8 mr-4">
              <a className="text-sm font-medium text-slate-400 hover:text-white transition-colors" href="#">Documentation</a>
              <a className="text-sm font-medium text-slate-400 hover:text-white transition-colors" href="#">System Status</a>
            </div>

            <div className="flex items-center space-x-2 bg-white/5 py-1.5 px-3 rounded-full border border-white/5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
              <span className="text-[10px] text-slate-300 font-bold tracking-wider uppercase">Active</span>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6 scroll-smooth">
          {initError ? (
             <div className="text-center text-red-400 bg-red-400/10 border border-red-400/20 p-4 rounded-xl text-sm max-w-lg mx-auto mt-10">{initError}</div>
          ) : messages.length === 0 && !isLoading ? (
             <div className="text-center text-slate-500 text-xs font-bold uppercase tracking-widest mt-20">Initializing secure connection...</div>
          ) : (
            messages.map((msg, idx) => (
              <MessageBubble 
                key={msg.id || msg.tempId || idx} 
                role={msg.role} 
                content={msg.content} 
              />
            ))
          )}
          {isLoading && (
            <MessageBubble role="agent" content="" isLoadingIndicator={true} />
          )}
          <div ref={endOfMessagesRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 sm:p-6 lg:p-8 bg-gradient-to-t from-[#0a0a0c] via-[#0a0a0c] to-transparent">
          <ChatInput onSendMessage={sendMessage} disabled={isLoading || !sessionId} />
        </div>

      </div>

    </div>
  );
};

export const ChatPage = () => {
  const [sessionId, setSessionId] = useState(null);

  return (
    <ChecklistProvider sessionId={sessionId}>
      <ChatPageInner sessionId={sessionId} setSessionId={setSessionId} />
    </ChecklistProvider>
  );
};
