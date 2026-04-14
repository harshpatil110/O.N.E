import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowRight, CheckCircle2, Clock } from 'lucide-react';
import { resendHrNotification } from '../api/adminApi';

export const SessionsTable = ({ sessions }) => {
  const [resendingId, setResendingId] = useState(null);

  const handleResend = async (sessionId) => {
    try {
      setResendingId(sessionId);
      await resendHrNotification(sessionId);
      alert('HR completion email sent successfully!');
    } catch (error) {
      console.error(error);
      alert('Failed to send email. Please check logs.');
    } finally {
      setResendingId(null);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const StatusBadge = ({ status }) => {
    if (status === 'completed') {
      return (
        <span className="inline-flex items-center gap-1.5 text-teal-700 bg-teal-50 px-2 py-1 text-sm border border-teal-200">
          <CheckCircle2 size={14} />
          Completed
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 text-amber-700 bg-amber-50 px-2 py-1 text-sm border border-amber-200">
        <Clock size={14} />
        In Progress
      </span>
    );
  };

  if (!sessions || sessions.length === 0) {
    return (
      <div className="bg-white border border-[#EAE8E2] text-center py-12 text-slate-500">
        No sessions found matching criteria.
      </div>
    );
  }

  return (
    <div className="bg-white border border-[#EAE8E2] overflow-x-auto">
      <table className="w-full text-left text-sm text-slate-600">
        <thead className="bg-[#F7F5F0] border-b border-[#EAE8E2] text-slate-800 uppercase tracking-wider text-xs">
          <tr>
            <th className="px-6 py-4 font-semibold">Employee</th>
            <th className="px-6 py-4 font-semibold">Role</th>
            <th className="px-6 py-4 font-semibold">Status</th>
            <th className="px-6 py-4 font-semibold">Started</th>
            <th className="px-6 py-4 font-semibold">Progress</th>
            <th className="px-6 py-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#EAE8E2]">
          {sessions.map((session) => (
            <tr key={session.session_id} className="hover:bg-slate-50 transition-colors">
              <td className="px-6 py-4">
                <div className="font-medium text-slate-900">{session.employee_name}</div>
                <div className="text-xs text-slate-500">{session.employee_email}</div>
              </td>
              <td className="px-6 py-4 text-slate-700">{session.role}</td>
              <td className="px-6 py-4">
                <StatusBadge status={session.status} />
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {formatDate(session.started_at)}
              </td>
              <td className="px-6 py-4">
                <div className="flex items-center gap-2">
                  <div className="w-full bg-[#EAE8E2] h-1.5 overflow-hidden">
                    <div 
                      className="bg-slate-800 h-1.5" 
                      style={{ width: `${session.percent_complete}%` }}
                    />
                  </div>
                  <span className="text-xs font-medium text-slate-700 tabular-nums">
                    {session.percent_complete}%
                  </span>
                </div>
              </td>
              <td className="px-6 py-4 text-right space-x-3 whitespace-nowrap">
                <Link 
                  to={`/dashboard/sessions/${session.session_id}`}
                  state={{ sessionSummary: session }}
                  className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 font-medium tracking-tight transition-colors"
                >
                  View <ArrowRight size={14} />
                </Link>
                
                {session.status === 'completed' && (
                  <button
                    onClick={() => handleResend(session.session_id)}
                    disabled={resendingId === session.session_id}
                    className="inline-flex items-center gap-1 text-slate-600 hover:text-slate-900 font-medium tracking-tight disabled:opacity-50 transition-colors"
                  >
                    <Mail size={14} />
                    {resendingId === session.session_id ? 'Sending...' : 'Resend'}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
