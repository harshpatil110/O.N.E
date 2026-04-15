import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useChat } from '../hooks/useChat';
import { startSession } from '../api/chat';
import { MessageBubble } from '../components/MessageBubble';
import { ChatInput } from '../components/ChatInput';
import { ChecklistSidebar } from '../components/ChecklistSidebar';
import { ChecklistProvider, useChecklist } from '../context/ChecklistContext';
import { PanelRightClose, PanelRightOpen } from 'lucide-react';

/**
 * Inner component that lives inside ChecklistProvider so it
 * can access the fetchProgress function from context.
 */
const ChatPageInner = ({ sessionId, setSessionId }) => {
  const [initError, setInitError] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const endOfMessagesRef = useRef(null);

  // Access the checklist context's refresh function
  const { fetchProgress } = useChecklist();

  // Wrap fetchProgress in a stable callback for useChat
  const handleMessageComplete = useCallback(() => {
    // Small delay to let the backend commit the DB changes
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
        
        // Try loading previous history
        const history = await loadHistory(sid);
        
        // Only append the initial greeting if there was no history loaded
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
    <div className="flex h-screen bg-[#F7F5F0] overflow-hidden font-sans">
      
      {/* LEFT PANEL: Chat Interface */}
      <div className={`flex flex-col border-r border-zinc-200 bg-white shadow-xl z-10 transition-all duration-300 ease-in-out ${isSidebarOpen ? 'w-[70%]' : 'w-full'}`}>
        
        {/* Header */}
        <div className="h-16 px-8 flex items-center border-b border-zinc-200">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-zinc-800">O.N.E. Identity Agent</h2>
          <div className="ml-auto flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-green-600"></span>
              <span className="text-xs text-zinc-500 font-medium tracking-wider uppercase">Active</span>
            </div>

            {/* Sidebar Toggle Button */}
            <button
              onClick={() => setIsSidebarOpen(prev => !prev)}
              className="p-2 text-zinc-400 hover:text-zinc-800 hover:bg-zinc-100 transition-all duration-200 border border-transparent hover:border-zinc-200"
              title={isSidebarOpen ? 'Hide sidebar' : 'Show sidebar'}
            >
              {isSidebarOpen ? <PanelRightClose size={18} /> : <PanelRightOpen size={18} />}
            </button>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8">
          {initError ? (
             <div className="text-center text-red-600 text-sm mt-10">{initError}</div>
          ) : messages.length === 0 && !isLoading ? (
             <div className="text-center text-zinc-400 text-sm mt-10 tracking-wide">Initializing secure connection...</div>
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
        <div className="px-8 pb-8 pt-4 bg-white">
          <ChatInput onSendMessage={sendMessage} disabled={isLoading || !sessionId} />
        </div>

      </div>

      {/* RIGHT PANEL: Checklist Sidebar */}
      <div className={`transition-all duration-300 ease-in-out overflow-hidden ${isSidebarOpen ? 'w-[30%] opacity-100' : 'w-0 opacity-0'}`}>
        {isSidebarOpen && <ChecklistSidebar />}
      </div>

    </div>
  );
};


/**
 * ChatPage wraps the inner component in the ChecklistProvider.
 * The sessionId state is lifted here so the provider can receive it.
 */
export const ChatPage = () => {
  const [sessionId, setSessionId] = useState(null);

  return (
    <ChecklistProvider sessionId={sessionId}>
      <ChatPageInner sessionId={sessionId} setSessionId={setSessionId} />
    </ChecklistProvider>
  );
};
