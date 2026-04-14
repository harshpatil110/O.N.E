import React, { useEffect, useState } from 'react';
import { getAdminMetrics, getAdminSessions } from '../api/adminApi';
import { MetricCard } from '../components/MetricCard';
import { SessionsTable } from '../components/SessionsTable';
import { LayoutDashboard, Filter } from 'lucide-react';

export const AdminDashboardPage = () => {
  const [metrics, setMetrics] = useState(null);
  const [sessionsData, setSessionsData] = useState({ items: [], total: 0 });
  const [loadingMetrics, setLoadingMetrics] = useState(true);
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [page, setPage] = useState(1);
  const [roleFilter, setRoleFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getAdminMetrics();
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load metrics', err);
        setError('Failed to load metrics. Keep calm and try again.');
      } finally {
        setLoadingMetrics(false);
      }
    };
    fetchMetrics();
  }, []);

  useEffect(() => {
    const fetchSessions = async () => {
      setLoadingSessions(true);
      try {
        const data = await getAdminSessions(page, 20, roleFilter, statusFilter);
        setSessionsData(data || { items: [], total: 0 });
      } catch (err) {
        console.error('Failed to load sessions', err);
        setError(`Failed to load sessions: ${err?.response?.data?.detail || err.message}`);
        setSessionsData({ items: [], total: 0 });
      } finally {
        setLoadingSessions(false);
      }
    };
    fetchSessions();
  }, [page, roleFilter, statusFilter]);

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-slate-900 font-sans p-8 md:p-12">
      <div className="max-w-7xl mx-auto space-y-12">
        
        {/* Header */}
        <header className="flex justify-between items-end border-b border-[#EAE8E2] pb-6">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight inline-flex items-center gap-3">
              <LayoutDashboard className="text-slate-400" />
              HR Administration
            </h1>
            <p className="text-slate-500 mt-2">Monitor onboarding metrics and progress globally.</p>
          </div>
        </header>

        {error && (
          <div className="bg-red-50 text-red-700 p-4 border border-red-200">
            {error}
          </div>
        )}

        {/* Metrics Grid */}
        <section>
          {loadingMetrics ? (
            <div className="text-slate-400 animate-pulse text-sm uppercase tracking-widest">
              Loading metrics...
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard 
                title="Total Sessions" 
                value={metrics?.total_sessions || 0} 
                colorScheme="slate"
              />
              <MetricCard 
                title="Active" 
                value={metrics?.active_sessions || 0} 
                colorScheme="amber"
              />
              <MetricCard 
                title="Completed" 
                value={metrics?.completed_sessions || 0}
                subtitle={`${metrics?.completions_this_week || 0} this week`}
                colorScheme="green"
              />
              <MetricCard 
                title="Avg Duration" 
                value={`${(metrics?.avg_duration_hours || 0).toFixed(1)}h`}
                subtitle="From start to finish"
                colorScheme="blue"
              />
            </div>
          )}
        </section>

        {/* Sessions Area */}
        <section className="space-y-6">
          <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4">
            <h2 className="text-xl font-medium tracking-tight">Onboarding Sessions</h2>
            
            {/* Filters */}
            <div className="flex flex-wrap items-center gap-4 text-sm">
              <div className="inline-flex items-center gap-2 text-slate-500">
                <Filter size={16} />
                Filters:
              </div>
              <select 
                className="bg-white border border-[#EAE8E2] px-3 py-1.5 focus:outline-none focus:border-slate-400"
                value={roleFilter}
                onChange={(e) => { setRoleFilter(e.target.value); setPage(1); }}
              >
                <option value="">All Roles</option>
                <option value="employee">Employee</option>
                <option value="hr_admin">HR Admin</option>
              </select>
              
              <select 
                className="bg-white border border-[#EAE8E2] px-3 py-1.5 focus:outline-none focus:border-slate-400"
                value={statusFilter}
                onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
              >
                <option value="">All Statuses</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>

          <div className="bg-white shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)] border border-[#EAE8E2]">
            {loadingSessions ? (
              <div className="p-12 text-center text-slate-400 text-sm uppercase tracking-widest animate-pulse">
                Fetching sessions...
              </div>
            ) : (
              <SessionsTable sessions={sessionsData.items} />
            )}
          </div>
          
          {/* Extremely minimalist pagination */}
          {!loadingSessions && sessionsData.total > 20 && (
            <div className="flex justify-between items-center text-sm">
              <div className="text-slate-500">
                Showing page {page} ({sessionsData.items.length} of {sessionsData.total} total)
              </div>
              <div className="space-x-4">
                <button 
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="font-medium text-slate-900 disabled:text-slate-400 tracking-tight"
                >
                  Previous
                </button>
                <button 
                  onClick={() => setPage(p => p + 1)}
                  disabled={page * 20 >= sessionsData.total}
                  className="font-medium text-slate-900 disabled:text-slate-400 tracking-tight"
                >
                  Next
                </button>
              </div>
            </div>
          )}

        </section>
      </div>
    </div>
  );
};
