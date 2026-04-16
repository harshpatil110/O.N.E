import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getProgress, updateChecklistItem } from '../api/checklist';

const ChecklistContext = createContext();

export const ChecklistProvider = ({ children, sessionId }) => {
  const [progress, setProgress] = useState({ total_items: 0, completed_count: 0, percent_complete: 0, items: [] });
  const [loading, setLoading] = useState(true);

  const fetchProgress = useCallback(async () => {
    if (!sessionId) {
      // Don't set loading=false here — we're still waiting for the session to be created.
      // The useEffect will re-trigger once sessionId becomes available.
      return;
    }
    try {
      const data = await getProgress(sessionId);
      if (data && data.items) {
        setProgress(data);
      }
    } catch (err) {
      console.error("Failed to fetch progress", err);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    // Reset loading state when sessionId changes
    if (sessionId) {
      setLoading(true);
      fetchProgress();
    }

    // Poll every 3 seconds for background updates (demo responsiveness)
    const interval = setInterval(fetchProgress, 3000);
    return () => clearInterval(interval);

  }, [fetchProgress, sessionId]);

  const markCurrentTaskDone = async () => {
    // Find the first task that is pending or in_progress
    const currentTaskIndex = progress.items.findIndex(item => item.status === 'pending' || item.status === 'in_progress');
    if (currentTaskIndex === -1) return;

    const currentTask = progress.items[currentTaskIndex];

    // Optimistic Update
    const updatedItems = [...progress.items];
    updatedItems[currentTaskIndex] = { ...currentTask, status: 'completed' };
    
    setProgress(prev => ({
      ...prev,
      items: updatedItems,
      completed_count: prev.completed_count + 1,
      percent_complete: Math.round(((prev.completed_count + 1) / prev.total_items) * 100)
    }));

    try {
      await updateChecklistItem(currentTask.id, 'completed');
      await fetchProgress(); // Refresh stats from server
    } catch (err) {
      console.error("Failed to mark task as done", err);
    }
  };

  return (
    <ChecklistContext.Provider value={{ progress, markCurrentTaskDone, fetchProgress, loading }}>
      {children}
    </ChecklistContext.Provider>
  );
};

export const useChecklist = () => useContext(ChecklistContext);
