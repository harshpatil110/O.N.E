import React, { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate, Link } from 'react-router-dom';
import { getProgress } from '../api/checklist';
import { getAdminSessions, resendHrNotification } from '../api/adminApi';
import { ChecklistItem } from '../components/ChecklistItem';
import { ArrowLeft, Mail, User as UserIcon } from 'lucide-react';

export const SessionDetailPage = () => {
  const { sessionId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [sessionSummary, setSessionSummary] = useState(location.state?.sessionSummary || null);
  const [checklistData, setChecklistData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSessionData = async () => {
      try {
        setLoading(true);

        // Fetch checklist items progress
         const progressData = await getProgress(sessionId);
         setChecklistData(progressData);

        // If no sessionSummary from router state, attempt to fetch it dynamically
        if (!sessionSummary) {
           const sessionsResp = await getAdminSessions(1, 100);
           const found = sessionsResp.items.find(s => s.session_id === sessionId);
           if (found) {
             setSessionSummary(found);
           }
        }
      } catch (err) {
        console.error(err);
        setError('Failed to fetch session details.');
      } finally {
        setLoading(false);
      }
    };
    fetchSessionData();
  }, [sessionId, sessionSummary]);

  const handleResend = async () => {
    try {
      setResending(true);
      await resendHrNotification(sessionId);
      alert('HR completion email sent successfully!');
    } catch (err) {
      console.error(err);
      alert('Failed to resend HR email.');
    } finally {
      setResending(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F7F5F0] text-slate-500 uppercase tracking-widest text-sm">
        Loading Details...
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#F7F5F0] p-8">
        <div className="bg-red-50 text-red-700 p-4 border border-red-200">
          {error}
        </div>
        <button onClick={() => navigate('/dashboard')} className="mt-4 text-slate-500 hover:text-slate-800 underline">
          &larr; Back to Dashboard
        </button>
      </div>
    );
  }

  const isCompleted = sessionSummary?.status === 'completed' || checklistData?.percent_complete === 100;

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-slate-900 font-sans p-8 md:p-12">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Navigation / Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#EAE8E2] pb-6">
          <div className="space-y-4">
            <Link to="/dashboard" className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-800 font-medium text-sm transition-colors">
              <ArrowLeft size={16} /> Back to Dashboard
            </Link>
            <h1 className="text-3xl font-semibold tracking-tight">Session Details</h1>
          </div>

          {isCompleted && (
            <button
              onClick={handleResend}
              disabled={resending}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 text-white text-sm font-medium hover:bg-slate-800 focus:ring-2 focus:ring-slate-900 focus:ring-offset-2 focus:ring-offset-[#F7F5F0] disabled:opacity-50 transition-all shadow-sm"
            >
              <Mail size={16} />
              {resending ? 'Sending Email...' : 'Resend HR Email'}
            </button>
          )}
        </div>

        {/* Employee Info Card */}
        {sessionSummary && (
          <div className="bg-white border border-[#EAE8E2] p-8 shadow-sm relative overflow-hidden">
            <div className="absolute top-0 left-0 w-1.5 h-full bg-slate-800" />
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-widest mb-6 inline-flex items-center gap-2">
              <UserIcon size={16} />
              Employee Information
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
               <div>
                 <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Name</div>
                 <div className="font-medium text-lg text-slate-900">{sessionSummary.employee_name}</div>
               </div>
               <div>
                 <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Email</div>
                 <div className="font-medium text-lg text-slate-900">{sessionSummary.employee_email}</div>
               </div>
               <div>
                 <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Role</div>
                 <div className="font-medium text-lg text-slate-900">{sessionSummary.role}</div>
               </div>
            </div>
          </div>
        )}

        {/* Checklist Section */}
        <div className="space-y-4">
           <h2 className="text-xl font-medium tracking-tight">Onboarding Checklist</h2>
           <div className="bg-[#EAE8E2] h-1.5 overflow-hidden w-full">
               <div 
                  className="bg-slate-800 h-1.5 transition-all duration-500" 
                  style={{ width: `${checklistData?.percent_complete || 0}%` }}
               />
           </div>
           
           <div className="flex justify-between items-center text-sm text-slate-500">
             <span>{checklistData?.completed_count || 0} of {checklistData?.total_items || 0} completed</span>
             <span className="font-semibold text-slate-900">{checklistData?.percent_complete || 0}%</span>
           </div>

           <div className="mt-6 space-y-3">
              {checklistData?.items?.map(item => (
                <ChecklistItem key={item.id} item={item} />
              ))}
              {(!checklistData?.items || checklistData.items.length === 0) && (
                 <div className="bg-white border border-[#EAE8E2] p-8 text-center text-slate-500">
                   No checklist items found for this session.
                 </div>
              )}
           </div>
        </div>

      </div>
    </div>
  );
};
