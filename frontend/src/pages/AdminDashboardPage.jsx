import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const AdminDashboardPage = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login");
    }

    return (
        <div className="min-h-screen bg-[#F7F5F0] flex flex-col items-center justify-center p-8">
            <h1 className="text-4xl font-light text-zinc-900 tracking-tight mb-4">Admin Dashboard</h1>
            <p className="text-zinc-600 mb-8 border-b border-zinc-200 pb-4">Secure Human Resources Environment</p>
            
            <button 
                onClick={handleLogout}
                className="px-6 py-2 bg-zinc-900 text-white text-xs font-medium uppercase tracking-widest hover:bg-zinc-800 transition-colors"
            >
                Secure Sign Out
            </button>
        </div>
    );
};
