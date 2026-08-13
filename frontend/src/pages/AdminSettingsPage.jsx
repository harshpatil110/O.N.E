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
                const token = sessionStorage.getItem('token');
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
            const token = sessionStorage.getItem('token');
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
        <div className="min-h-screen bg-[#F7F5F0] text-stone-900 font-sans flex">
            {/* Sidebar */}
            <aside className="w-64 border-r border-stone-200 bg-[#F2F0EA] flex flex-col hidden md:flex flex-shrink-0">
                <div className="p-6 border-b border-stone-200">
                    <div className="flex items-center gap-2.5 font-serif font-bold text-stone-900 text-lg tracking-tight">
                        <div className="w-7 h-7 rounded-sm bg-stone-900 flex items-center justify-center text-stone-100 font-mono text-xs">O</div>
                        O.N.E. <span className="font-sans text-xs uppercase font-mono tracking-widest text-stone-400">Admin</span>
                    </div>
                </div>

                <nav className="flex-1 px-4 space-y-1 mt-6 text-xs font-medium">
                    {navItems.map(item => {
                        const isActive = location.pathname === item.to;
                        return (
                            <Link
                                key={item.to}
                                to={item.to}
                                className={`px-3 py-2.5 rounded-sm flex items-center gap-3 transition-colors ${
                                    isActive
                                        ? 'bg-stone-900 text-stone-100 shadow-sm'
                                        : 'text-stone-600 hover:text-stone-900 hover:bg-stone-200/60'
                                }`}
                            >
                                <item.icon size={16} />
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-stone-200">
                    <Link to="/admin/settings" className="flex items-center gap-3 px-2 py-2 rounded-sm hover:bg-stone-200/60 cursor-pointer transition-colors">
                        <div className="w-7 h-7 rounded-sm bg-stone-200 flex flex-shrink-0 items-center justify-center text-stone-800 text-xs font-mono font-bold border border-stone-300">
                            {profile ? getInitials(profile.name) : <UserIcon size={14} />}
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-xs font-semibold text-stone-900 truncate">{profile?.name || 'Loading...'}</p>
                            <p className="text-[10px] text-stone-500 font-mono truncate capitalize">{profile?.role?.replace('_', ' ') || '...'}</p>
                        </div>
                        <Settings size={14} className="text-stone-400" />
                    </Link>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto overflow-x-hidden">
                <div className="px-8 py-10 w-full max-w-2xl mx-auto space-y-8">
                    {/* Page Header */}
                    <div>
                        <h1 className="text-2xl font-serif font-bold tracking-tight text-stone-900 mb-1">Admin Profile Settings</h1>
                        <p className="text-xs font-mono uppercase tracking-widest text-stone-500">Manage your account details and preferences.</p>
                    </div>

                    {loading ? (
                        <div className="w-full h-64 bg-white border border-stone-200 rounded-md shadow-sm flex flex-col items-center justify-center animate-pulse">
                            <div className="size-8 rounded-full border-2 border-stone-300 border-t-stone-900 animate-spin mb-3" />
                            <p className="text-xs font-mono uppercase tracking-widest text-stone-500">Loading Profile...</p>
                        </div>
                    ) : error ? (
                        <div className="bg-rose-50 border border-rose-200 text-rose-800 p-4 rounded-sm text-xs font-mono flex items-center gap-3">
                            <AlertTriangle size={16} />
                            {error}
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-6">
                            {/* Profile Card */}
                            <div className="bg-white border border-stone-200 rounded-md p-8 shadow-sm space-y-6">
                                {/* Avatar + Name Header */}
                                <div className="flex items-center gap-4">
                                    <div className="w-14 h-14 rounded-sm bg-stone-100 border border-stone-300 flex items-center justify-center text-stone-900 text-lg font-mono font-bold">
                                        {getInitials(formName)}
                                    </div>
                                    <div>
                                        <h2 className="text-base font-serif font-bold text-stone-900">{formName || 'Your Name'}</h2>
                                        <p className="text-xs font-mono text-stone-500 capitalize">{profile?.role?.replace('_', ' ') || 'Admin'}</p>
                                    </div>
                                </div>

                                {/* Divider */}
                                <div className="border-t border-stone-100" />

                                {/* Full Name */}
                                <div className="space-y-1.5">
                                    <label htmlFor="settings-name" className="block text-[10px] font-mono font-bold text-stone-500 uppercase tracking-widest">Full Name</label>
                                    <input
                                        id="settings-name"
                                        type="text"
                                        value={formName}
                                        onChange={(e) => setFormName(e.target.value)}
                                        className="w-full bg-white text-stone-900 text-xs rounded-sm px-3.5 py-2.5 outline-none border border-stone-300 focus:border-stone-900 transition-colors placeholder:text-stone-400 font-medium"
                                        placeholder="Enter your name"
                                    />
                                </div>

                                {/* Email */}
                                <div className="space-y-1.5">
                                    <label htmlFor="settings-email" className="block text-[10px] font-mono font-bold text-stone-500 uppercase tracking-widest">Email Address</label>
                                    <input
                                        id="settings-email"
                                        type="email"
                                        value={formEmail}
                                        onChange={(e) => setFormEmail(e.target.value)}
                                        className="w-full bg-white text-stone-900 text-xs rounded-sm px-3.5 py-2.5 outline-none border border-stone-300 focus:border-stone-900 transition-colors placeholder:text-stone-400 font-medium"
                                        placeholder="Enter your email"
                                    />
                                </div>

                                {/* Role (Read-Only) */}
                                <div className="space-y-1.5">
                                    <label htmlFor="settings-role" className="block text-[10px] font-mono font-bold text-stone-500 uppercase tracking-widest">Role</label>
                                    <input
                                        id="settings-role"
                                        type="text"
                                        value={profile?.role?.replace('_', ' ').toUpperCase() || ''}
                                        disabled
                                        className="w-full bg-stone-100 text-stone-500 text-xs font-mono rounded-sm px-3.5 py-2.5 outline-none border border-stone-200 cursor-not-allowed uppercase"
                                    />
                                    <p className="text-[10px] font-mono text-stone-400">Role is managed by the system and cannot be changed here.</p>
                                </div>
                            </div>

                            {/* Success Message */}
                            {successMsg && (
                                <div className="flex items-center gap-3 bg-emerald-50 border border-emerald-200 text-emerald-800 px-4 py-3 rounded-sm text-xs font-mono">
                                    <CheckCircle size={14} />
                                    {successMsg}
                                </div>
                            )}

                            {/* Error Message */}
                            {saveError && (
                                <div className="flex items-center gap-3 bg-rose-50 border border-rose-200 text-rose-800 px-4 py-3 rounded-sm text-xs font-mono">
                                    <AlertTriangle size={14} />
                                    {saveError}
                                </div>
                            )}

                            {/* Submit Button */}
                            <div className="flex justify-end">
                                <button
                                    type="submit"
                                    disabled={isSaving}
                                    className={`text-white text-xs font-mono font-bold uppercase tracking-widest px-5 py-2.5 rounded-sm flex items-center gap-2 transition-colors shadow-sm ${
                                        isSaving
                                            ? 'bg-stone-700 cursor-wait opacity-70'
                                            : 'bg-stone-900 hover:bg-stone-800'
                                    }`}
                                >
                                    {isSaving ? (
                                        <>
                                            <Loader2 size={14} className="animate-spin" />
                                            Saving...
                                        </>
                                    ) : (
                                        <>
                                            <Save size={14} />
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
