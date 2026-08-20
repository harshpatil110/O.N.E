import React, { useState, useEffect } from 'react';
import { fetchDevelopers, fetchUserChatHistory } from '../services/adminService';
import { ChatTranscriptModal } from '../components/ChatTranscriptModal';

export const AdminDevelopersPage = () => {
  const [developers, setDevelopers] = useState([]);
  const [loading, setLoading] = useState(true);

  const [isChatModalOpen, setIsChatModalOpen] = useState(false);
  const [selectedDeveloper, setSelectedDeveloper] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [loadingChats, setLoadingChats] = useState(false);

  useEffect(() => {
    const loadDevelopers = async () => {
      try {
        setLoading(true);
        const devsData = await fetchDevelopers();
        setDevelopers(devsData);
      } catch (err) {
        console.error('Error loading developers:', err);
      } finally {
        setLoading(false);
      }
    };
    loadDevelopers();
  }, []);

  const handleViewChats = async (dev) => {
    setSelectedDeveloper(dev);
    setIsChatModalOpen(true);
    setLoadingChats(true);
    setChatMessages([]);
    
    try {
        const response = await fetchUserChatHistory(dev.id);
        
        // Strictly target the 'logs' array from our new standardized backend response
        if (response && response.status === "success" && Array.isArray(response.logs)) {
            setChatMessages(response.logs);
        } else {
            console.warn("[UI] Response did not contain a valid logs array", response);
            setChatMessages([]);
        }
    } catch (error) {
        console.error("[UI] Error setting messages:", error);
        setChatMessages([]);
    } finally {
        setLoadingChats(false);
    }
  };

  return (
    <>
      <div className="min-h-screen p-8 bg-[#FBF9F5] text-[#1A1A1A]">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold font-serif tracking-tight text-[#1A1A1A] mb-1">Developer Directory</h1>
            <p className="text-xs font-mono uppercase tracking-widest text-[#7A756D]">Live overview of onboarding progression and access statuses.</p>
          </div>
        </div>

        <div className="bg-[#FFFFFF] border border-[#E5E0D8] p-6 shadow-none">
          <div className="divide-y divide-[#E5E0D8]">
            {loading ? (
              <div className="py-8 text-center text-xs font-mono text-[#7A756D]">Loading developers...</div>
            ) : developers.length === 0 ? (
              <div className="py-8 text-center text-xs font-mono text-[#7A756D]">No developers found.</div>
            ) : (
              developers.map((dev) => (
                <div key={dev.id} className="py-4 flex items-center justify-between text-sm">
                  <div className="w-1/4">
                    <p className="font-medium text-[#1A1A1A]">{dev.name}</p>
                    <p className="text-xs text-[#7A756D]">{dev.email || 'No email'}</p>
                    <p className="text-[10px] uppercase tracking-widest text-[#7A756D] mt-1">{dev.role || 'Developer'}</p>
                  </div>
                  <div className="w-1/4 text-xs text-[#7A756D]">
                    {dev.progress === 0 ? 'Awaiting Checklist' : 'In Progress'}
                  </div>
                  <div className="w-1/4 flex items-center space-x-3">
                    <div className="w-full bg-[#E5E0D8] h-1.5 rounded-full overflow-hidden">
                      <div 
                        className="bg-[#1A1A1A] h-full transition-all duration-300" 
                        style={{ width: `${dev.progress || 0}%` }}
                      />
                    </div>
                    <span className="text-xs font-mono w-10 text-right">{dev.progress || 0}%</span>
                  </div>
                  <div className="w-1/4 text-right">
                    <button
                      onClick={() => handleViewChats(dev)}
                      className="text-xs font-medium text-[#1A1A1A] hover:bg-[#E5E0D8] transition-colors border border-[#E5E0D8] px-3 py-1.5 rounded-none bg-white uppercase tracking-wider cursor-pointer"
                    >
                      View Chats
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
      
      <ChatTranscriptModal 
        isOpen={isChatModalOpen} 
        onClose={() => setIsChatModalOpen(false)} 
        developer={selectedDeveloper} 
        messages={chatMessages} 
        loading={loadingChats} 
      />
    </>
  );
};
