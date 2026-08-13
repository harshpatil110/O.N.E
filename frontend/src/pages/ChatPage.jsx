import React, { useEffect, useState, useRef, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { useChat } from '../hooks/useChat';
import { startSession } from '../api/chat';
import { MessageBubble } from '../components/MessageBubble';
import { ChatInput } from '../components/ChatInput';
import { ChecklistProvider, useChecklist } from '../context/ChecklistContext';
import { useAuth } from '../hooks/useAuth';

const ChatPageInner = ({ sessionId, setSessionId }) => {
  const [initError, setInitError] = useState(null);
  const endOfMessagesRef = useRef(null);
  const { fetchProgress } = useChecklist();
  const { user } = useAuth();

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
    <div className="flex h-full w-full bg-[#F7F5F0] text-stone-900 overflow-hidden font-sans selection:bg-blue-100">
      
      {/* Editorial Grid Pattern */}
      <div 
        className="absolute inset-0 z-0 pointer-events-none opacity-40"
        style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, #E7E5E4 1px, transparent 0)',
          backgroundSize: '20px 20px'
        }}
      />

      {/* LEFT PANEL: Chat Interface */}
      <div className="relative flex flex-col z-10 w-full h-full">
        
        {/* Header */}
        <div className="h-16 px-6 lg:px-12 flex items-center justify-between border-b border-stone-200 bg-[#F7F5F0]/90 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <div className="size-7 bg-stone-900 rounded-sm flex items-center justify-center text-stone-100 shadow-sm">
              <span className="font-bold font-mono text-xs tracking-tighter">O.</span>
            </div>
            <h2 className="text-stone-900 text-lg font-serif font-bold tracking-tight">O.N.E.</h2>
            <span className="text-[10px] font-mono uppercase tracking-widest text-stone-400 border-l border-stone-200 pl-3">Onboarding System</span>
          </div>
          <div className="flex items-center gap-3">
            {user?.onboardingProgress > 0 ? (
              <Link to="/checklist" className="text-xs font-mono uppercase tracking-widest text-stone-500 hover:text-stone-900 transition-colors">
                My Checklist
              </Link>
            ) : (
              <span className="text-[10px] font-mono uppercase tracking-widest text-stone-400 font-semibold bg-[#F7F5F0] px-2.5 py-1.5 rounded-sm border border-stone-200 flex items-center gap-1.5 shadow-sm">
                <svg className="size-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8V7z" />
                </svg>
                Gate Locked
              </span>
            )}
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6 scroll-smooth">
          {initError ? (
             <div className="text-center text-rose-700 bg-rose-50 border border-rose-200 p-4 rounded-md text-xs font-mono max-w-lg mx-auto mt-10">{initError}</div>
          ) : messages.length === 0 && !isLoading ? (
             <div className="text-center text-stone-400 text-xs font-mono uppercase tracking-widest mt-20">Initializing secure session...</div>
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
        <div className="p-4 sm:p-6 lg:p-8 bg-[#F7F5F0] border-t border-stone-200/60">
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
