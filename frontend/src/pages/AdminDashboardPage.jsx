import React, { useState, useEffect } from 'react';
import { fetchDashboardStats, fetchDevelopers } from '../services/adminService';

export const AdminDashboardPage = () => {
  const [stats, setStats] = useState({
    total_developers: 0,
    average_completion_rate: 0,
    stuck_developers: 0,
    avg_time_to_onboard_days: 0
  });
  const [developers, setDevelopers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        const [statsData, devsData] = await Promise.all([
          fetchDashboardStats(),
          fetchDevelopers()
        ]);
        setStats(statsData);
        setDevelopers(devsData);
      } catch (err) {
        console.error('Error loading admin dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboardData();
  }, []);

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
            <a href="/admin" className="flex items-center px-4 py-3 bg-[#1A1A1A] text-white text-sm transition-colors rounded-sm">
              <span className="mr-3 text-lg opacity-80">⊞</span> Dashboard
            </a>
            
            <a href="/admin/developers" className="flex items-center px-4 py-3 text-[#1A1A1A] hover:bg-[#F2EFE9] text-sm transition-colors rounded-sm">
              <span className="mr-3 text-lg opacity-60">👥</span> Developers
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
        <div className="min-h-screen p-8 space-y-8 bg-[#FBF9F5] text-[#1A1A1A]">
          {/* 1. Top KPI Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="border border-[#E5E0D8] p-6 bg-[#FFFFFF] rounded-none">
              <span className="text-xs uppercase tracking-widest text-[#7A756D]">Developers Onboarding</span>
              <div className="text-4xl font-serif mt-2 font-normal">{stats.total_developers}</div>
            </div>

            <div className="border border-[#E5E0D8] p-6 bg-[#FFFFFF] rounded-none">
              <span className="text-xs uppercase tracking-widest text-[#7A756D]">Average Completion Rate</span>
              <div className="text-4xl font-serif mt-2 font-normal">{stats.average_completion_rate}%</div>
            </div>

            <div className="border border-[#E5E0D8] p-6 bg-[#FFFFFF] rounded-none">
              <span className="text-xs uppercase tracking-widest text-[#7A756D]">Avg. Time to Onboard</span>
              <div className="text-4xl font-serif mt-2 font-normal">{stats.avg_time_to_onboard_days} <span className="text-base font-sans">days</span></div>
            </div>
          </div>

          {/* 2. Dynamic Status Advisory Banner */}
          {stats.stuck_developers > 0 && (
            <div className="border border-[#F2C0B6] bg-[#FDF2F0] p-4 flex items-center justify-between">
              <div className="flex items-center space-x-3 text-[#B83A2A] text-sm">
                <span className="font-semibold">Status Advisory:</span>
                <span>{stats.stuck_developers} developer(s) currently at 0% progress awaiting onboarding initialization.</span>
              </div>
            </div>
          )}

          {/* 3. Live Onboarding Progress Table */}
          <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6">
            <h2 className="text-xl font-serif mb-4">Onboarding Progress</h2>
            <div className="divide-y divide-[#E5E0D8]">
              {developers.map((dev) => (
                <div key={dev.id} className="py-4 flex items-center justify-between text-sm">
                  <div className="w-1/4">
                    <p className="font-medium text-[#1A1A1A]">{dev.name}</p>
                    <p className="text-xs text-[#7A756D]">{dev.role || 'Developer'}</p>
                  </div>
                  <div className="w-1/4 text-xs text-[#7A756D]">
                    {dev.progress === 0 ? 'Awaiting Checklist' : 'In Progress'}
                  </div>
                  <div className="w-1/3 flex items-center space-x-3">
                    <div className="w-full bg-[#E5E0D8] h-1.5 rounded-full overflow-hidden">
                      <div 
                        className="bg-[#1A1A1A] h-full transition-all duration-300" 
                        style={{ width: `${dev.progress || 0}%` }}
                      />
                    </div>
                    <span className="text-xs font-mono w-10 text-right">{dev.progress || 0}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
