import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';

export const DashboardLayout = () => {
  return (
    <div className="flex h-screen w-full bg-[#F7F5F0] overflow-hidden font-sans">
      <Sidebar />
      <main className="flex-1 relative overflow-hidden">
        <Outlet />
      </main>
    </div>
  );
};
