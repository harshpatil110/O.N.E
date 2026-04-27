import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { 
  BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis,
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import { 
  Search, Bell, Plus, LayoutDashboard, Users, BarChart2, MessageSquare, Settings, User as UserIcon, AlertTriangle
} from 'lucide-react';

export const AdminAnalyticsPage = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isExporting, setIsExporting] = useState(false);
    const dashboardRef = useRef(null);

    const handleExportPDF = async () => {
        if (!dashboardRef.current || isExporting) return;
        setIsExporting(true);
        try {
            const canvas = await html2canvas(dashboardRef.current, {
                backgroundColor: '#0B0B0E',
                scale: 2,
                useCORS: true,
                logging: false,
            });
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF('l', 'mm', 'a4');
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = pdf.internal.pageSize.getHeight();
            const canvasRatio = canvas.height / canvas.width;
            const imgWidth = pdfWidth - 20;
            const imgHeight = imgWidth * canvasRatio;

            if (imgHeight <= pdfHeight - 20) {
                pdf.addImage(imgData, 'PNG', 10, 10, imgWidth, imgHeight);
            } else {
                let yOffset = 0;
                let pageIndex = 0;
                const pageImgHeight = pdfHeight - 20;
                const sourceSliceHeight = pageImgHeight / imgWidth * canvas.width;

                while (yOffset < canvas.height) {
                    if (pageIndex > 0) pdf.addPage();
                    const sliceCanvas = document.createElement('canvas');
                    sliceCanvas.width = canvas.width;
                    sliceCanvas.height = Math.min(sourceSliceHeight, canvas.height - yOffset);
                    const ctx = sliceCanvas.getContext('2d');
                    ctx.drawImage(canvas, 0, yOffset, canvas.width, sliceCanvas.height, 0, 0, sliceCanvas.width, sliceCanvas.height);
                    const sliceImg = sliceCanvas.toDataURL('image/png');
                    const sliceDisplayHeight = sliceCanvas.height / canvas.width * imgWidth;
                    pdf.addImage(sliceImg, 'PNG', 10, 10, imgWidth, sliceDisplayHeight);
                    yOffset += sourceSliceHeight;
                    pageIndex++;
                }
            }
            pdf.save('ONE_Analytics_Report.pdf');
        } catch (err) {
            console.error('PDF export failed:', err);
        } finally {
            setIsExporting(false);
        }
    };

    useEffect(() => {
        const fetchAnalytics = async () => {
             try {
                 const token = localStorage.getItem('token');
                 const res = await axios.get('http://localhost:8000/api/v1/hr/analytics/deep-dive', {
                     headers: { Authorization: `Bearer ${token}` },
                     withCredentials: true
                 });
                 setData(res.data);
             } catch (err) {
                 console.error("Failed to load AI analytics payload", err);
                 setError("Failed to fetch analytics deep-dive data.");
             } finally {
                 setLoading(false);
             }
        };
        fetchAnalytics();
    }, []);

    // Combine for ScatterChart: Developer Proficiency Matrix
    const scatterData = [];
    if (data?.quantitative?.completion_matrix && data?.qualitative?.developer_insights) {
        data.quantitative.completion_matrix.forEach(comp => {
            const insight = data.qualitative.developer_insights.find(i => i.developer_id === comp.developer_id);
            if (insight) {
                scatterData.push({
                    name: comp.employee_name,
                    percent_complete: comp.percent_complete,
                    question_complexity_score: insight.question_complexity_score,
                    question_severity: insight.question_severity
                });
            }
        });
    }

    const COLORS = ['#6366f1', '#34d399', '#fb7185', '#22d3ee', '#fbbf24'];

    const getSeverityColor = (severity) => {
        if (severity === 'High') return '#fb7185';
        if (severity === 'Medium') return '#fbbf24';
        return '#34d399';
    };

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
                <Link to="/dashboard" className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3">
                    <LayoutDashboard size={18} />
                    Dashboard
                </Link>
                <Link to="/admin/developers" className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3">
                    <Users size={18} />
                    Developers
                </Link>
                <Link to="/admin/analytics" className="px-3 py-2.5 rounded-lg bg-indigo-600/10 text-indigo-400 flex items-center gap-3 cursor-pointer">
                    <BarChart2 size={18} />
                    Analytics
                </Link>
                <div className="px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#13131A] transition-colors flex items-center gap-3 cursor-pointer">
                    <MessageSquare size={18} />
                    AI Insights
                </div>
                </nav>

                <div className="p-4 border-t border-white/5">
                <div className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-[#13131A] cursor-pointer transition-colors">
                    <div className="w-8 h-8 rounded-full bg-slate-800 flex flex-shrink-0 items-center justify-center text-slate-300">
                        <UserIcon size={16} />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-white truncate">Alex Chen</p>
                        <p className="text-xs text-slate-500 truncate">Manager Mode</p>
                    </div>
                    <Settings size={16} className="text-slate-500" />
                </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto overflow-x-hidden">
                {/* Header */}
                <header className="px-8 py-6 flex flex-col md:flex-row md:justify-between items-center gap-4">
                    <div className="relative w-full md:w-96">
                        <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                        <input 
                            type="text" 
                            placeholder="Search dashboards or metrics..." 
                            className="w-full bg-[#13131A] text-sm text-white placeholder-slate-500 rounded-full pl-10 pr-4 py-2.5 outline-none border border-white/5 focus:border-indigo-500/50 transition-colors shadow-sm"
                        />
                    </div>
                    <div className="flex items-center gap-5">
                        <button className="relative text-slate-400 hover:text-white transition-colors">
                            <Bell size={20} />
                        </button>
                        <button
                            onClick={handleExportPDF}
                            disabled={isExporting || loading}
                            className={`text-white text-sm font-medium px-5 py-2.5 rounded-full flex items-center gap-2 transition-colors shadow-lg shadow-indigo-600/20 ${
                                isExporting ? 'bg-indigo-800 cursor-wait opacity-70' : 'bg-indigo-600 hover:bg-indigo-500'
                            }`}
                        >
                            {isExporting ? (
                                <>
                                    <div className="w-4 h-4 rounded-full border-2 border-white/30 border-t-white animate-spin" />
                                    Generating PDF...
                                </>
                            ) : (
                                <>
                                    <Plus size={16} strokeWidth={3} />
                                    Export Data
                                </>
                            )}
                        </button>
                    </div>
                </header>

                <div ref={dashboardRef} className="px-8 pb-12 w-full max-w-7xl mx-auto space-y-8">
                    {/* Header Title */}
                    <div>
                        <h1 className="text-2xl font-bold tracking-tight text-white mb-1">Analytics & AI Insights</h1>
                        <p className="text-sm font-medium text-slate-500">Qualitative and quantitative diagnostics powered by LLM.</p>
                    </div>

                    {loading ? (
                         <div className="w-full h-64 bg-[#13131A] border border-white/5 rounded-xl shadow-xl flex flex-col items-center justify-center animate-pulse">
                              <div className="size-10 rounded-full border-4 border-indigo-500/30 border-t-indigo-500 animate-spin mb-4" />
                              <p className="text-sm font-bold uppercase tracking-widest text-indigo-400">AI Processing Chat Transcripts & Aggregating Metrics...</p>
                         </div>
                    ) : error ? (
                        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm flex items-center gap-3">
                            <AlertTriangle size={16} />
                            {error}
                        </div>
                    ) : (
                        <>
                            {/* AI Insights Alert Banner */}
                            {data?.qualitative?.lagging_developer && data.qualitative.lagging_developer.developer_id && (
                                <section className="bg-rose-900/20 border border-rose-500/30 rounded-xl p-5 shadow-[0_0_20px_rgba(251,113,133,0.05)]">
                                    <div className="flex items-start gap-4">
                                        <div className="w-10 h-10 rounded-full bg-rose-500/20 flex items-center justify-center text-rose-400 flex-shrink-0">
                                            <AlertTriangle size={20} />
                                        </div>
                                        <div>
                                            <h3 className="text-rose-200 font-bold tracking-wide flex items-center gap-2">
                                                Intervention Required <span className="px-2 py-0.5 rounded text-[10px] font-black tracking-widest bg-rose-500 text-white uppercase">Critical</span>
                                            </h3>
                                            <p className="text-rose-200/80 text-sm mt-1 leading-relaxed">
                                                {data.qualitative.lagging_developer.risk_summary}
                                            </p>
                                        </div>
                                    </div>
                                </section>
                            )}

                            {/* Dense Visualization Grid */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                
                                {/* Chart 1: Cohort Progress */}
                                <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl flex flex-col h-[400px]">
                                    <h3 className="text-white text-sm font-bold tracking-wide mb-6">Cohort Progress Tracker</h3>
                                    <div className="flex-1 w-full min-h-0">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <BarChart data={data?.quantitative?.completion_matrix || []}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                                                <XAxis dataKey="employee_name" stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} tickLine={false} axisLine={false} />
                                                <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} tickLine={false} axisLine={false} domain={[0, 100]} />
                                                <Tooltip 
                                                    cursor={{fill: '#ffffff05'}}
                                                    contentStyle={{backgroundColor: '#0B0B0E', borderColor: '#ffffff10', borderRadius: '8px', color: '#fff'}}
                                                    itemStyle={{color: '#6366f1'}}
                                                />
                                                <Bar dataKey="percent_complete" fill="#6366f1" radius={[4, 4, 0, 0]} maxBarSize={40} />
                                            </BarChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>

                                {/* Chart 2: Task Velocity */}
                                <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl flex flex-col h-[400px]">
                                    <h3 className="text-white text-sm font-bold tracking-wide mb-6">Task Velocity (Avg Hours)</h3>
                                    <div className="flex-1 w-full min-h-0">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <AreaChart data={data?.quantitative?.task_velocity || []}>
                                                <defs>
                                                    <linearGradient id="colorVelocity" x1="0" y1="0" x2="0" y2="1">
                                                        <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3}/>
                                                        <stop offset="95%" stopColor="#22d3ee" stopOpacity={0}/>
                                                    </linearGradient>
                                                </defs>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                                                <XAxis dataKey="title" stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 10}} tickLine={false} axisLine={false} tickFormatter={(val) => val.length > 15 ? val.substring(0, 15) + '...' : val} />
                                                <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} tickLine={false} axisLine={false} />
                                                <Tooltip 
                                                    contentStyle={{backgroundColor: '#0B0B0E', borderColor: '#ffffff10', borderRadius: '8px', color: '#fff'}}
                                                    itemStyle={{color: '#22d3ee'}}
                                                />
                                                <Area type="monotone" dataKey="avg_duration_hours" stroke="#22d3ee" strokeWidth={3} fillOpacity={1} fill="url(#colorVelocity)" />
                                            </AreaChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>

                                {/* Chart 3: Topic Distribution */}
                                <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl flex flex-col h-[400px]">
                                    <h3 className="text-white text-sm font-bold tracking-wide mb-6">AI Conversational Topic Distribution</h3>
                                    <div className="flex-1 w-full min-h-0 relative">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <PieChart>
                                                <Pie
                                                    data={data?.qualitative?.topic_distribution || []}
                                                    dataKey="percentage"
                                                    nameKey="topic"
                                                    cx="50%"
                                                    cy="50%"
                                                    innerRadius={80}
                                                    outerRadius={110}
                                                    stroke="none"
                                                    paddingAngle={5}
                                                >
                                                    {(data?.qualitative?.topic_distribution || []).map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                    ))}
                                                </Pie>
                                                <Tooltip 
                                                    contentStyle={{backgroundColor: '#0B0B0E', borderColor: '#ffffff10', borderRadius: '8px', color: '#fff'}}
                                                    itemStyle={{color: '#fff'}}
                                                    formatter={(value) => `${value}%`}
                                                />
                                            </PieChart>
                                        </ResponsiveContainer>
                                        {/* Inner Label */}
                                        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                                            <span className="text-2xl font-bold text-white tracking-tight">100%</span>
                                            <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">Topics</span>
                                        </div>
                                    </div>
                                </div>

                                {/* Chart 4: Proficiency Matrix */}
                                <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl flex flex-col h-[400px]">
                                    <h3 className="text-white text-sm font-bold tracking-wide mb-6">Developer Proficiency Matrix</h3>
                                    <div className="flex-1 w-full min-h-0">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                                                <XAxis type="number" dataKey="percent_complete" name="Progression" unit="%" stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} domain={[0, 100]} />
                                                <YAxis type="number" dataKey="question_complexity_score" name="Complexity Score" stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} domain={[1, 10]} />
                                                <ZAxis type="category" dataKey="name" name="Developer" />
                                                <Tooltip 
                                                    cursor={{strokeDasharray: '3 3', stroke: '#ffffff30'}}
                                                    contentStyle={{backgroundColor: '#0B0B0E', borderColor: '#ffffff10', borderRadius: '8px', color: '#fff'}}
                                                    formatter={(value, name) => {
                                                        if (name === "Developer") return [value, name];
                                                        if (name === "Complexity Score") return [value, name];
                                                        return [value, "Progression"];
                                                    }}
                                                />
                                                <Scatter name="Developers" data={scatterData}>
                                                    {
                                                        scatterData.map((entry, index) => (
                                                            <Cell key={`cell-${index}`} fill={getSeverityColor(entry.question_severity)} />
                                                        ))
                                                    }
                                                </Scatter>
                                            </ScatterChart>
                                        </ResponsiveContainer>
                                        <div className="flex justify-center gap-6 mt-4">
                                            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#fb7185]"></div><span className="text-[10px] uppercase font-bold text-slate-500">High Severity</span></div>
                                            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#fbbf24]"></div><span className="text-[10px] uppercase font-bold text-slate-500">Med Severity</span></div>
                                            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#34d399]"></div><span className="text-[10px] uppercase font-bold text-slate-500">Low Severity</span></div>
                                        </div>
                                    </div>
                                </div>

                                {/* Chart 5: Developer Frustration Index */}
                                <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl flex flex-col h-[400px]">
                                    <h3 className="text-white text-sm font-bold tracking-wide mb-6">Developer Frustration Index</h3>
                                    <div className="flex-1 w-full min-h-0">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <BarChart data={data?.qualitative?.sentiment_index || []}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                                                <XAxis dataKey="employee_name" stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} tickLine={false} axisLine={false} />
                                                <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8', fontSize: 12}} tickLine={false} axisLine={false} domain={[0, 100]} />
                                                <Tooltip 
                                                    cursor={{fill: '#ffffff05'}}
                                                    contentStyle={{backgroundColor: '#0B0B0E', borderColor: '#ffffff10', borderRadius: '8px', color: '#fff'}}
                                                    itemStyle={{color: '#fff'}}
                                                    formatter={(value, name, props) => {
                                                        const emotion = props.payload.primary_emotion || 'Unknown';
                                                        return [`${value} (${emotion})`, 'Frustration Level'];
                                                    }}
                                                />
                                                <Bar dataKey="frustration_score" radius={[4, 4, 0, 0]} maxBarSize={40}>
                                                    {(data?.qualitative?.sentiment_index || []).map((entry, index) => {
                                                        let color = '#6366f1'; // Indigo
                                                        if (entry.frustration_score > 70) color = '#fb7185'; // Rose
                                                        if (entry.frustration_score < 30) color = '#34d399'; // Emerald
                                                        return <Cell key={`cell-${index}`} fill={color} />;
                                                    })}
                                                </Bar>
                                            </BarChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>

                                {/* Chart 6: Autonomy vs AI Reliance */}
                                <div className="bg-[#13131A] border border-white/5 rounded-xl p-6 shadow-xl flex flex-col h-[400px]">
                                    <h3 className="text-white text-sm font-bold tracking-wide mb-6">Autonomy vs. AI Reliance</h3>
                                    <div className="flex-1 w-full min-h-0">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data?.qualitative?.autonomy_scores || []}>
                                                <PolarGrid stroke="#ffffff20" />
                                                <PolarAngleAxis dataKey="employee_name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                                                <PolarRadiusAxis angle={30} domain={[0, 10]} tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
                                                <Tooltip 
                                                    contentStyle={{backgroundColor: '#0B0B0E', borderColor: '#ffffff10', borderRadius: '8px', color: '#fff'}}
                                                    itemStyle={{color: '#22d3ee'}}
                                                />
                                                <Radar name="Independence Rating" dataKey="independence_rating" stroke="#22d3ee" fill="#22d3ee" fillOpacity={0.2} strokeWidth={2} />
                                            </RadarChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>

                            </div>
                        </>
                    )}
                </div>
            </main>
        </div>
    );
};
