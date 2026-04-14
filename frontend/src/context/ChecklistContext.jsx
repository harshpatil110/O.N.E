import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getProgress, updateChecklistItem } from '../api/checklist';

const ChecklistContext = createContext();

export const ChecklistProvider = ({ children, sessionId }) => {
  const [progress, setProgress] = useState({ total_items: 0, completed_count: 0, percent_complete: 0, items: [] });
  const [loading, setLoading] = useState(true);

  const fetchProgress = useCallback(async () => {
    if (!sessionId) return;
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
    fetchProgress();
    // Poll every 10 seconds for background updates
    const interval = setInterval(fetchProgress, 10000);
    return () => clearInterval(interval);
  }, [fetchProgress]);

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

    setLoading(true);
    try {
      await updateChecklistItem(currentTask.id, 'completed');
      await fetchProgress(); // Refresh stats from server
    } catch (err) {
      console.error("Failed to mark task as done", err);
      // Optional: rollback on error, but for the demo we can leave it
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChecklistContext.Provider value={{ progress, markCurrentTaskDone, fetchProgress, loading }}>
      {children}
    </ChecklistContext.Provider>
  );
};

export const useChecklist = () => useContext(ChecklistContext);
