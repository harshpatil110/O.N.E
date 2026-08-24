import React, { useState, useEffect } from 'react';
import { fetchPendingVerifications, verifyDeveloperTask } from '../services/adminService';
import { useNavigate } from 'react-router-dom';

export default function TaskVerification() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState(null);
  
  const navigate = useNavigate();
  
  const loadTasks = async () => {
    try {
      setLoading(true);
      const res = await fetchPendingVerifications();
      if (res.status === 'success') setTasks(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial load with loading spinner
    loadTasks();

    // Silent background polling every 5 seconds
    const intervalId = setInterval(async () => {
      try {
        const res = await fetchPendingVerifications();
        if (res.status === 'success') setTasks(res.data);
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 5000);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  const handleVerify = async (taskId) => {
    try {
      await verifyDeveloperTask(taskId);
      setSelectedTask(null);
      loadTasks(); // Refresh list after approval
    } catch (err) {
      console.error("Verification failed", err);
    }
  };

  return (
      <div className="flex flex-col h-full overflow-hidden">
        <header className="h-16 border-b border-[#E5E0D8] bg-[#FFFFFF] flex items-center px-8 justify-between shrink-0">
          <div className="flex items-center text-sm font-mono text-[#7A756D]">
            <span>/</span>
            <span className="mx-2 text-[#1A1A1A]">admin</span>
            <span>/</span>
            <span className="mx-2 text-[#1A1A1A]">verification</span>
          </div>
          <div className="text-xs font-mono text-[#7A756D]">
            STATUS: <span className="text-[#1A1A1A]">HUMAN-IN-THE-LOOP ACTIVE</span>
          </div>
        </header>

        <div className="p-8 space-y-8 bg-[#FBF9F5] text-[#1A1A1A] flex-1 overflow-y-auto">
          <div>
            <h1 className="text-2xl font-serif">Task Verification</h1>
            <p className="text-xs font-mono uppercase text-[#7A756D] mt-2">Human-in-the-loop task validation.</p>
          </div>

          <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-0 rounded-none shadow-none">
            {loading ? (
              <p className="p-6 text-xs font-mono text-[#7A756D]">Loading pending tasks...</p>
            ) : tasks.length === 0 ? (
              <p className="p-6 text-xs font-mono text-[#7A756D]">No tasks currently pending verification.</p>
            ) : (
              <div className="divide-y divide-[#E5E0D8]">
                {tasks.map((task) => (
                  <div key={task.task_id} className="p-6 flex items-center justify-between">
                    <div>
                      <p className="font-serif text-[#1A1A1A]">{task.task_name}</p>
                      <p className="text-xs font-mono text-[#7A756D] mt-1">Submitted by: {task.user_name}</p>
                    </div>
                    <button 
                      onClick={() => setSelectedTask(task)}
                      className="px-4 py-2 border border-[#1A1A1A] text-[#1A1A1A] text-xs font-mono uppercase hover:bg-[#1A1A1A] hover:text-white transition-colors"
                    >
                      Review Task
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* THE AI INSIGHT MODAL */}
          {selectedTask && (
            <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
              <div className="bg-[#FAF8F5] border border-[#E5E0D8] w-full max-w-2xl flex flex-col p-8 shadow-none rounded-none">
                
                <div className="flex items-center justify-between border-b border-[#E5E0D8] pb-4 mb-6">
                  <div>
                    <h3 className="font-serif text-xl text-[#1A1A1A]">AI Performance Review</h3>
                    <p className="text-xs font-mono uppercase text-[#7A756D] mt-1">
                      Developer: {selectedTask.user_name} | Task: {selectedTask.task_name}
                    </p>
                  </div>
                  <button onClick={() => setSelectedTask(null)} className="text-sm font-mono text-[#7A756D] hover:text-[#1A1A1A]">✕ Close</button>
                </div>

                <div className="space-y-6">
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-widest text-[#1A1A1A] mb-2">Speed Analysis</h4>
                    <p className="text-sm font-sans text-[#1A1A1A] p-4 bg-[#FFFFFF] border border-[#E5E0D8]">{selectedTask.speed_analysis}</p>
                  </div>
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-widest text-[#1A1A1A] mb-2">Learning Curve</h4>
                    <p className="text-sm font-sans text-[#1A1A1A] p-4 bg-[#FFFFFF] border border-[#E5E0D8]">{selectedTask.learning_curve}</p>
                  </div>
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-widest text-[#1A1A1A] mb-2">Mistakes Made</h4>
                    <p className="text-sm font-sans text-[#1A1A1A] p-4 bg-[#FFFFFF] border border-[#E5E0D8]">{selectedTask.mistakes_made}</p>
                  </div>
                </div>

                <div className="mt-8 pt-6 border-t border-[#E5E0D8] flex justify-end space-x-4">
                  <button 
                    onClick={() => setSelectedTask(null)}
                    className="px-6 py-3 text-xs font-mono uppercase text-[#7A756D] hover:text-[#1A1A1A]"
                  >
                    Cancel
                  </button>
                  <button 
                    onClick={() => handleVerify(selectedTask.task_id)}
                    className="px-6 py-3 bg-[#1A1A1A] text-white text-xs font-mono uppercase border border-[#1A1A1A] hover:bg-[#333333] transition-colors"
                  >
                    Approve & Verify Task
                  </button>
                </div>

              </div>
            </div>
          )}
        </div>
      </div>
  );
}
