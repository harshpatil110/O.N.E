import React from 'react';

// Transcript Modal Component
export function ChatTranscriptModal({ isOpen, onClose, developer, messages, loading }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-[#FAF8F5] border border-[#E5E0D8] w-full max-w-2xl max-h-[80vh] flex flex-col p-6 shadow-none">
        <div className="flex items-center justify-between border-b border-[#E5E0D8] pb-4 mb-4">
          <div>
            <h3 className="font-serif text-lg text-[#1A1A1A]">Chat Transcript</h3>
            <p className="text-xs text-[#7A756D]">History with {developer?.name || developer?.email}</p>
          </div>
          <button onClick={onClose} className="text-sm font-mono text-[#7A756D] hover:text-[#1A1A1A]">✕ Close</button>
        </div>

        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {loading ? (
            <p className="text-xs text-[#7A756D] font-mono text-center py-8">Loading transcripts...</p>
          ) : messages.length === 0 ? (
            <p className="text-xs text-[#7A756D] font-mono text-center py-8">No conversation logs found for this developer.</p>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                <span className="text-[10px] font-mono uppercase text-[#7A756D] mb-1">
                  {msg.role === 'user' ? (developer?.name || 'Developer') : 'O.N.E. Assistant'}
                </span>
                <div className={`p-3 text-xs max-w-[85%] border ${
                  msg.role === 'user' 
                    ? 'bg-[#EBF3FC] border-[#CFE1F7] text-[#1A1A1A]' 
                    : 'bg-[#FFFFFF] border-[#E5E0D8] text-[#1A1A1A]'
                }`}>
                  {/* Strictly use msg.message as defined in the backend dictionary */}
                  {msg.message}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
