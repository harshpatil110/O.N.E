import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

export const AdminLayout = () => {
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
            <NavLink 
              to="/admin" 
              end
              className={({ isActive }) => 
                `flex items-center px-4 py-3 text-sm transition-colors rounded-sm ${isActive ? 'bg-[#1A1A1A] text-white' : 'text-[#1A1A1A] hover:bg-[#F2EFE9]'}`
              }
            >
              {({ isActive }) => (
                <>
                  <span className={`mr-3 text-lg ${isActive ? 'opacity-80' : 'opacity-60'}`}>⊞</span> Dashboard
                </>
              )}
            </NavLink>
            
            <NavLink 
              to="/admin/developers" 
              className={({ isActive }) => 
                `flex items-center px-4 py-3 text-sm transition-colors rounded-sm ${isActive ? 'bg-[#1A1A1A] text-white' : 'text-[#1A1A1A] hover:bg-[#F2EFE9]'}`
              }
            >
              {({ isActive }) => (
                <>
                  <span className={`mr-3 text-lg ${isActive ? 'opacity-80' : 'opacity-60'}`}>👥</span> Developers
                </>
              )}
            </NavLink>
            
            <NavLink 
              to="/admin/verification" 
              className={({ isActive }) => 
                `flex items-center px-4 py-3 text-sm transition-colors rounded-sm ${isActive ? 'bg-[#1A1A1A] text-white' : 'text-[#1A1A1A] hover:bg-[#F2EFE9]'}`
              }
            >
              {({ isActive }) => (
                <>
                  <span className={`mr-3 text-lg ${isActive ? 'opacity-80' : 'opacity-60'}`}>✓</span> Task Verification
                </>
              )}
            </NavLink>
            
            <NavLink 
              to="/admin/analytics" 
              className={({ isActive }) => 
                `flex items-center px-4 py-3 text-sm transition-colors rounded-sm ${isActive ? 'bg-[#1A1A1A] text-white' : 'text-[#1A1A1A] hover:bg-[#F2EFE9]'}`
              }
            >
              {({ isActive }) => (
                <>
                  <span className={`mr-3 text-lg ${isActive ? 'opacity-80' : 'opacity-60'}`}>📊</span> Analytics
                </>
              )}
            </NavLink>
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
        <Outlet />
      </main>
    </div>
  );
};
