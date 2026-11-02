import React, { useState, useEffect } from 'react';

export function TaskProofModal({ isOpen, onClose, task, userEmail, onSubmit, submitting }) {
  const [githubRepoUrl, setGithubRepoUrl] = useState('');
  const [proofNotes, setProofNotes] = useState('');
  const [screenshots, setScreenshots] = useState([]);
  const [subtasks, setSubtasks] = useState([
    {
      number: 1,
      title: 'Clone Repository & Configure Local Dev Environment',
      tier: 'Tier 3: Proof-of-Work Validated',
      weight: 90,
      badgeColor: 'border-emerald-300 bg-emerald-50 text-emerald-800'
    },
    {
      number: 2,
      title: 'System / MCP Telemetry & Environment Check',
      tier: 'Tier 1: System/MCP Verified',
      weight: 100,
      badgeColor: 'border-emerald-300 bg-emerald-50 text-emerald-800'
    },
    {
      number: 3,
      title: 'Verify Swagger /docs 200 OK & Service Health Check',
      tier: 'Tier 3: Proof-of-Work Validated',
      weight: 90,
      badgeColor: 'border-emerald-300 bg-emerald-50 text-emerald-800'
    },
    {
      number: 4,
      title: 'Architecture Standards & Developer Self-Attestation',
      tier: 'Tier 6: Self-Attestation',
      weight: 60,
      badgeColor: 'border-amber-300 bg-amber-50 text-amber-800'
    }
  ]);

  // Reset form when opened for a new task
  useEffect(() => {
    if (isOpen) {
      setGithubRepoUrl('');
      setProofNotes('');
      setScreenshots([]);
    }
  }, [isOpen, task?.id]);

  if (!isOpen) return null;

  // Handle multiple image uploads and convert to Base64 data URLs via FileReader
  const handleImageChange = (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (uploadEvent) => {
        const base64Data = uploadEvent.target.result;
        setScreenshots(prev => [...prev, base64Data]);
      };
      reader.readAsDataURL(file);
    });
  };

  const removeScreenshot = (index) => {
    setScreenshots(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    onSubmit({
      githubRepoUrl: githubRepoUrl.trim(),
      proofNotes: proofNotes.trim(),
      screenshots,
    });
  };

  const handleSkip = () => {
    onSubmit({
      githubRepoUrl: '',
      proofNotes: 'Developer completed via self-attestation.',
      screenshots: [],
    });
  };

  return (
    <div className="fixed inset-0 bg-stone-900/40 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-150">
      <div className="bg-[#FAF8F5] border border-[#E5E0D8] w-full max-w-2xl max-h-[90vh] flex flex-col shadow-xl rounded-sm overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-5 border-b border-[#E5E0D8] bg-[#F7F5F0] flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[10px] font-mono uppercase tracking-widest px-1.5 py-0.5 bg-stone-900 text-stone-100 rounded-sm">
                Step {task?.sequence || 1}
              </span>
              <span className="text-[10px] font-mono uppercase tracking-widest text-stone-400">Proof-of-Work Verification</span>
            </div>
            <h3 className="font-serif text-xl font-normal text-stone-900 tracking-tight">
              {task?.task_name || 'Verify Task Completion'}
            </h3>
          </div>
          <button 
            type="button"
            onClick={onClose} 
            className="size-8 flex items-center justify-center text-stone-400 hover:text-stone-900 transition-colors text-lg"
          >
            ✕
          </button>
        </div>

        {/* Modal Scrollable Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* 6-Tier Subtask Verification Target Overview */}
          <div className="bg-white border border-[#E5E0D8] p-4 rounded-sm">
            <div className="flex items-center justify-between mb-3 border-b border-stone-100 pb-2">
              <span className="text-xs font-mono uppercase tracking-wider text-stone-700 font-semibold">
                6-Tier Subtask Verification Criteria
              </span>
              <span className="text-xs font-mono text-emerald-700 font-medium bg-emerald-50 px-2 py-0.5 border border-emerald-200 rounded-sm">
                Target: 85.0% Confidence
              </span>
            </div>
            
            <div className="space-y-2">
              {subtasks.map((st) => (
                <div key={st.number} className="flex items-center justify-between text-xs py-1 border-b border-stone-50 last:border-0">
                  <div className="flex items-center gap-2 flex-1 pr-3">
                    <span className="font-mono text-stone-400 text-[11px]">{st.number}.</span>
                    <span className="text-stone-800">{st.title}</span>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`text-[10px] font-mono px-2 py-0.5 border rounded-sm ${st.badgeColor}`}>
                      {st.tier}
                    </span>
                    <span className="font-mono text-[10px] text-stone-500 w-8 text-right font-medium">
                      {st.weight}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* 1. Upload Screenshots */}
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-stone-700 mb-1.5 font-medium">
                Upload Proof Screenshots (Optional)
              </label>
              <div className="border border-dashed border-[#D6D0C4] bg-white hover:bg-stone-50/50 transition-colors p-4 rounded-sm text-center">
                <input
                  type="file"
                  id="proof-screenshots"
                  accept="image/*"
                  multiple
                  onChange={handleImageChange}
                  className="hidden"
                />
                <label 
                  htmlFor="proof-screenshots" 
                  className="cursor-pointer flex flex-col items-center justify-center gap-1.5"
                >
                  <svg className="size-6 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span className="text-xs text-stone-600 font-sans">
                    Click to select screenshots (<span className="font-mono text-stone-400">PNG, JPG, WebP</span>)
                  </span>
                  <span className="text-[10px] font-mono text-stone-400">Stored instantly as Base64 for instant demo display</span>
                </label>
              </div>

              {/* Thumbnails Preview */}
              {screenshots.length > 0 && (
                <div className="mt-3 grid grid-cols-3 sm:grid-cols-4 gap-2.5">
                  {screenshots.map((src, index) => (
                    <div key={index} className="relative group border border-stone-200 rounded-sm overflow-hidden bg-white aspect-video flex items-center justify-center">
                      <img 
                        src={src} 
                        alt={`Proof ${index + 1}`} 
                        className="object-cover w-full h-full"
                      />
                      <button
                        type="button"
                        onClick={() => removeScreenshot(index)}
                        className="absolute top-1 right-1 size-5 bg-stone-900/80 text-white hover:bg-stone-900 rounded-full flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity"
                        title="Remove image"
                      >
                        ✕
                      </button>
                      <span className="absolute bottom-1 left-1 bg-stone-900/70 text-white font-mono text-[9px] px-1 rounded-xs">
                        #{index + 1}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* 2. GitHub Repo / PR URL */}
            <div>
              <label htmlFor="github-repo-url" className="block text-xs font-mono uppercase tracking-wider text-stone-700 mb-1.5 font-medium">
                GitHub Repository / PR Link (Optional)
              </label>
              <input
                id="github-repo-url"
                type="url"
                value={githubRepoUrl}
                onChange={(e) => setGithubRepoUrl(e.target.value)}
                placeholder="https://github.com/organization/repo/pull/1"
                className="w-full px-3 py-2 text-xs font-mono bg-white border border-[#D6D0C4] rounded-sm focus:outline-none focus:border-stone-800 text-stone-900 placeholder:text-stone-400"
              />
            </div>

            {/* 3. CLI / Swagger Output / Verification Notes */}
            <div>
              <label htmlFor="proof-notes" className="block text-xs font-mono uppercase tracking-wider text-stone-700 mb-1.5 font-medium">
                CLI / Swagger Output / Verification Notes (Optional)
              </label>
              <textarea
                id="proof-notes"
                rows={3}
                value={proofNotes}
                onChange={(e) => setProofNotes(e.target.value)}
                placeholder="e.g. curl -i http://localhost:8000/docs -> HTTP/1.1 200 OK&#10;Git commit: 8f4a12c pushed to feature branch."
                className="w-full px-3 py-2 text-xs font-mono bg-white border border-[#D6D0C4] rounded-sm focus:outline-none focus:border-stone-800 text-stone-900 placeholder:text-stone-400 resize-none"
              />
            </div>
          </form>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-[#E5E0D8] bg-[#F7F5F0] flex items-center justify-between">
          <button
            type="button"
            onClick={handleSkip}
            disabled={submitting}
            className="text-[11px] font-mono uppercase tracking-wider text-stone-500 hover:text-stone-900 transition-colors disabled:opacity-50"
          >
            Skip Proof (Self-Attestation)
          </button>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="px-4 py-2 text-xs font-mono uppercase tracking-wider text-stone-600 hover:text-stone-900 transition-colors"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={submitting}
              className={`px-5 py-2.5 text-xs font-mono uppercase tracking-widest text-[#F7F5F0] rounded-sm shadow-sm transition-colors ${
                submitting
                  ? 'bg-stone-500 cursor-wait'
                  : 'bg-stone-900 hover:bg-stone-800'
              }`}
            >
              {submitting ? 'Submitting Proof...' : 'Submit Proof & Complete Task'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

