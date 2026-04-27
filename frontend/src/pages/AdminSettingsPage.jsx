import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Users, BarChart2, Settings, User as UserIcon,
  Save, Loader2, CheckCircle, AlertTriangle
} from 'lucide-react';

export const AdminSettingsPage = () => {
    const location = useLocation();

    // Profile state
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Form state
    const [formName, setFormName] = useState('');
    const [formEmail, setFormEmail] = useState('');
    const [isSaving, setIsSaving] = useState(false);
    const [successMsg, setSuccessMsg] = useState('');
    const [saveError, setSaveError] = useState('');

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:8000/api/v1/admin/profile', {
                    headers: { Authorization: `Bearer ${token}` },
                    withCredentials: true,
                });
                setProfile(res.data);
                setFormName(res.data.name || '');
                setFormEmail(res.data.email || '');
            } catch (err) {
                console.error('Failed to load admin profile', err);
                setError('Failed to fetch profile data.');
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    const getInitials = (name) => {
        if (!name) return '?';
        return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSaving(true);
        setSuccessMsg('');
        setSaveError('');

        try {
            const token = localStorage.getItem('token');
            const res = await axios.put(
                'http://localhost:8000/api/v1/admin/profile',
                { name: formName, email: formEmail },
                {
                    headers: { Authorization: `Bearer ${token}` },
                    withCredentials: true,
                }
            );
            setProfile(res.data);
            setSuccessMsg('Profile updated successfully.');
            setTimeout(() => setSuccessMsg(''), 4000);
        } catch (err) {
            console.error('Profile update failed:', err);
            const detail = err.response?.data?.detail || 'Failed to update profile. Please try again.';
            setSaveError(detail);
            setTimeout(() => setSaveError(''), 5000);
        } finally {
            setIsSaving(false);
        }
    };

    const navItems = [
        { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
        { to: '/admin/developers', icon: Users, label: 'Developers' },
        { to: '/admin/analytics', icon: BarChart2, label: 'Analytics' },
        { to: '/admin/settings', icon: Settings, label: 'Settings' },
    ];

    return (
        <div className="min-h-screen bg-[#0B0B0E] text-slate-400 font-sans flex">
            {/* Sidebar */}
            <aside className="w-64 border-r border-white/5 bg-[#0B0B0E] flex flex-col hidden md:flex flex-shrink-0">
                <div className="p-6 border-b border-white/5">
                    <div className="flex items-center gap-2 font-semibold text-white text-lg tracking-wide">
                        <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">O</div>
                        O.N.E. <span className="text-indigo-500">Admin</span>
                    </div>
                </div>

                <nav className="flex-1 px-4 space-y-2 mt-6 text-sm font-medium">
                    {navItems.map(item => {
                        const isActive = location.pathname === item.to;
                        return (
                            <Link
                                key={item.to}
                                to={item.to}
                                className={`px-3 py-2.5 rounded-lg flex items-center gap-3 transition-colors ${
                                    isActive
                                        ? 'bg-indigo-600/10 text-indigo-400'
                                        : 'text-slate-400 hover:text-white hover:bg-[#13131A]'
                                }`}
                            >
                                <item.icon size={18} />
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-white/5">
                    <Link to="/admin/settings" className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-[#13131A] cursor-pointer transition-colors">
                        <div className="w-8 h-8 rounded-full bg-indigo-600/20 flex flex-shrink-0 items-center justify-center text-indigo-400 text-xs font-bold">
                            {profile ? getInitials(profile.name) : <UserIcon size={16} />}
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-white truncate">{profile?.name || 'Loading...'}</p>
                            <p className="text-xs text-slate-500 truncate capitalize">{profile?.role?.replace('_', ' ') || '...'}</p>
                        </div>
                        <Settings size={16} className="text-slate-500" />
                    </Link>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto overflow-x-hidden">
                <div className="px-8 py-10 w-full max-w-2xl mx-auto space-y-8">
                    {/* Page Header */}
                    <div>
                        <h1 className="text-2xl font-bold tracking-tight text-white mb-1">Admin Profile Settings</h1>
                        <p className="text-sm font-medium text-slate-500">Manage your account details and preferences.</p>
                    </div>

                    {loading ? (
                        <div className="w-full h-64 bg-[#13131A] border border-white/5 rounded-xl shadow-xl flex flex-col items-center justify-center animate-pulse">
                            <div className="size-10 rounded-full border-4 border-indigo-500/30 border-t-indigo-500 animate-spin mb-4" />
                            <p className="text-sm font-bold uppercase tracking-widest text-indigo-400">Loading Profile...</p>
                        </div>
                    ) : error ? (
                        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm flex items-center gap-3">
                            <AlertTriangle size={16} />
                            {error}
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-6">
                            {/* Profile Card */}
                            <div className="bg-[#13131A] border border-white/5 rounded-xl p-8 shadow-xl space-y-8">
                                {/* Avatar + Name Header */}
                                <div className="flex items-center gap-5">
                                    <div className="w-16 h-16 rounded-full bg-indigo-600/20 border-2 border-indigo-500/30 flex items-center justify-center text-indigo-400 text-xl font-bold tracking-wide">
                                        {getInitials(formName)}
                                    </div>
                                    <div>
                                        <h2 className="text-lg font-semibold text-white">{formName || 'Your Name'}</h2>
                                        <p className="text-sm text-slate-500 capitalize">{profile?.role?.replace('_', ' ') || 'Admin'}</p>
                                    </div>
                                </div>

                                {/* Divider */}
                                <div className="border-t border-white/5" />

                                {/* Full Name */}
                                <div className="space-y-2">
                                    <label htmlFor="settings-name" className="block text-sm font-medium text-slate-400">Full Name</label>
                                    <input
                                        id="settings-name"
                                        type="text"
                                        value={formName}
                                        onChange={(e) => setFormName(e.target.value)}
                                        className="w-full bg-[#0B0B0E] text-white text-sm rounded-lg px-4 py-3 outline-none border border-white/5 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all placeholder-slate-600"
                                        placeholder="Enter your name"
                                    />
                                </div>

                                {/* Email */}
                                <div className="space-y-2">
                                    <label htmlFor="settings-email" className="block text-sm font-medium text-slate-400">Email Address</label>
                                    <input
                                        id="settings-email"
                                        type="email"
                                        value={formEmail}
                                        onChange={(e) => setFormEmail(e.target.value)}
                                        className="w-full bg-[#0B0B0E] text-white text-sm rounded-lg px-4 py-3 outline-none border border-white/5 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all placeholder-slate-600"
                                        placeholder="Enter your email"
                                    />
                                </div>

                                {/* Role (Read-Only) */}
                                <div className="space-y-2">
                                    <label htmlFor="settings-role" className="block text-sm font-medium text-slate-400">Role</label>
                                    <input
                                        id="settings-role"
                                        type="text"
                                        value={profile?.role?.replace('_', ' ').toUpperCase() || ''}
                                        disabled
                                        className="w-full bg-white/5 text-slate-500 text-sm rounded-lg px-4 py-3 outline-none border border-white/5 cursor-not-allowed capitalize"
                                    />
                                    <p className="text-xs text-slate-600">Role is managed by the system and cannot be changed here.</p>
                                </div>
                            </div>

                            {/* Success Message */}
                            {successMsg && (
                                <div className="flex items-center gap-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-4 py-3 rounded-xl text-sm font-medium animate-in fade-in">
                                    <CheckCircle size={16} />
                                    {successMsg}
                                </div>
                            )}

                            {/* Error Message */}
                            {saveError && (
                                <div className="flex items-center gap-3 bg-rose-500/10 border border-rose-500/20 text-rose-400 px-4 py-3 rounded-xl text-sm font-medium">
                                    <AlertTriangle size={16} />
                                    {saveError}
                                </div>
                            )}

                            {/* Submit Button */}
                            <div className="flex justify-end">
                                <button
                                    type="submit"
                                    disabled={isSaving}
                                    className={`text-white text-sm font-medium px-6 py-3 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-indigo-600/20 ${
                                        isSaving
                                            ? 'bg-indigo-800 cursor-wait opacity-70'
                                            : 'bg-indigo-600 hover:bg-indigo-500'
                                    }`}
                                >
                                    {isSaving ? (
                                        <>
                                            <Loader2 size={16} className="animate-spin" />
                                            Saving...
                                        </>
                                    ) : (
                                        <>
                                            <Save size={16} />
                                            Update Profile
                                        </>
                                    )}
                                </button>
                            </div>
                        </form>
                    )}
                </div>
            </main>
        </div>
    );
};
