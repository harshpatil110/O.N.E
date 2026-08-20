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
    <div className="flex h-screen w-full bg-[#FBF9F5] text-[#1A1A1A] font-sans">
      
      {/* RESTORED LEFT SIDEBAR */}
      <aside className="w-64 bg-[#FBF9F5] border-r border-[#E5E0D8] flex flex-col justify-between hidden md:flex">
        
        {/* Top Section: Logo & Nav */}
        <div>
          {/* Logo */}
          <div className="h-20 flex items-center px-6 border-b border-[#E5E0D8]">
            <div className="bg-[#1A1A1A] text-white text-xs font-mono px-2 py-1 mr-3">0.</div>
            <h1 className="font-serif text-lg tracking-wide font-medium">O.N.E. <span className="text-xs font-sans text-[#7A756D] ml-1 tracking-widest">ADMIN</span></h1>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-2 mt-4">
            <a href="/admin" className="flex items-center px-4 py-3 text-[#1A1A1A] hover:bg-[#F2EFE9] text-sm transition-colors rounded-sm">
              <span className="mr-3 text-lg opacity-60">⊞</span> Dashboard
            </a>
            
            <a href="/admin/developers" className="flex items-center px-4 py-3 bg-[#1A1A1A] text-white text-sm transition-colors rounded-sm">
              <span className="mr-3 text-lg opacity-80">👥</span> Developers
            </a>
            
            {/* Inactive State (Task Verification) */}
            <a href="/admin/verification" className="flex items-center px-4 py-3 text-[#1A1A1A] hover:bg-[#F2EFE9] text-sm transition-colors rounded-none">
              <span className="mr-3 text-lg opacity-60">✓</span> Task Verification
            </a>
            
            <a href="/admin/analytics" className="flex items-center px-4 py-3 text-[#1A1A1A] hover:bg-[#F2EFE9] text-sm transition-colors rounded-sm">
              <span className="mr-3 text-lg opacity-60">📊</span> Analytics
            </a>
          </nav>
        </div>

        {/* Bottom Section: Admin Profile */}
        <div className="p-6 border-t border-[#E5E0D8] flex items-center">
          <div className="w-10 h-10 bg-[#E5E0D8] flex items-center justify-center font-mono text-xs text-[#1A1A1A] mr-3 rounded-sm">
            MA
          </div>
          <div>
            <p className="text-sm font-medium">Master Admin</p>
            <p className="text-xs text-[#7A756D]">Admin</p>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 h-screen overflow-y-auto">
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
      
      </main>
    </div>
  );
};
