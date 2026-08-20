import React, { useState, useEffect } from 'react';
import { fetchAnalyticsTopics, fetchDevelopers, fetchAIInsights, fetchAdvancedAnalytics } from '../services/adminService';
import { 
  PieChart, Pie, Cell, 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, 
  ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  ScatterChart, Scatter, ZAxis,
  LineChart, Line
} from 'recharts';

export const AdminAnalyticsPage = () => {
  const [topicData, setTopicData] = useState([]);
  const [devData, setDevData] = useState([]);
  const [insights, setInsights] = useState(null);
  const [advancedData, setAdvancedData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Strictly Muted, Print-Inspired Palette (No Neon)
  const COLORS = ['#1A1A1A', '#5C6B73', '#9DB4C0', '#C2DFE3', '#E0A96D'];

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setLoading(true);
        const [topics, devs, insightsData, advanced] = await Promise.all([
          fetchAnalyticsTopics(),
          fetchDevelopers(),
          fetchAIInsights(),
          fetchAdvancedAnalytics()
        ]);
        
        setInsights(insightsData);
        setAdvancedData(advanced);
        
        // Format Topic Data for Recharts PieChart
        if (topics && topics.percentages) {
          const formattedTopics = Object.keys(topics.percentages).map(key => ({
            name: key.replace('_', ' ').toUpperCase(),
            value: topics.percentages[key],
            raw: topics.raw_counts[key]
          })).filter(item => item.raw > 0); // Only show active categories
          setTopicData(formattedTopics);
        }

        // Format Developer Data for BarChart
        setDevData(devs);
      } catch (err) {
        console.error('Error loading analytics:', err);
      } finally {
        setLoading(false);
      }
    };
    loadAnalytics();
  }, []);

  // Custom Tooltip adhering to structural minimalism (no drop shadows)
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-[#FBF9F5] border border-[#E5E0D8] p-3 rounded-none shadow-none">
          <p className="text-xs font-mono uppercase text-[#7A756D]">{payload[0].name || payload[0].dataKey || (payload[0].payload && payload[0].payload.name)}</p>
          <p className="text-sm font-serif text-[#1A1A1A] mt-1">
            {payload[0].value} {payload[0].payload && payload[0].payload.raw !== undefined && <span className="text-xs font-sans text-[#7A756D]">({payload[0].payload.raw} queries)</span>}
          </p>
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[80vh] w-full bg-[#FBF9F5] p-8">
        {/* Structural Loading Container */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-10 w-full max-w-md flex flex-col items-center">
          
          {/* Top Brand Element */}
          <div className="flex items-center space-x-3 mb-8">
            <div className="bg-[#1A1A1A] text-white text-xs font-mono px-2 py-1">0.</div>
            <h1 className="font-serif text-xl tracking-wide text-[#1A1A1A]">O.N.E. <span className="text-xs font-sans text-[#7A756D] ml-1 tracking-widest uppercase">Engine</span></h1>
          </div>

          {/* Minimalist Progress Track (Replaces generic spinners) */}
          <div className="w-full h-[1px] bg-[#E5E0D8] relative overflow-hidden mb-6">
            <div className="absolute top-0 left-0 h-full bg-[#1A1A1A] w-1/3 animate-[slideRight_2s_ease-in-out_infinite_alternate]"></div>
          </div>

          {/* Typography-Driven Status Output */}
          <div className="flex flex-col items-center space-y-2">
            <p className="text-xs font-mono uppercase tracking-widest text-[#1A1A1A] animate-pulse">
              Compiling Diagnostics
            </p>
            <p className="text-[10px] font-mono text-[#7A756D]">
              Aggregating LLM insights and cohort matrices...
            </p>
          </div>

        </div>
        
        {/* Decorative Grid Lines to anchor the container (Editorial feel) */}
        <div className="w-px h-24 bg-[#E5E0D8] mt-8"></div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 bg-[#FBF9F5] text-[#1A1A1A] min-h-screen">
      <div>
        <h1 className="text-2xl font-serif">Analytics & AI Insights</h1>
        <p className="text-xs font-mono uppercase text-[#7A756D] mt-2">Quantitative diagnostics powered by LLM.</p>
      </div>

      {/* Dynamic Advisory Banner */}
      {insights && (
        <div className={`border p-4 flex items-center justify-between ${
          insights.advisory_level === 'CRITICAL' ? 'border-[#F2C0B6] bg-[#FDF2F0] text-[#B83A2A]' :
          insights.advisory_level === 'WARNING' ? 'border-[#EAE1C5] bg-[#FDFBF2] text-[#917624]' :
          'border-[#C2DFE3] bg-[#F0F7F9] text-[#2F6168]'
        }`}>
          <div className="flex items-center space-x-3 text-sm">
            <span className="font-semibold uppercase tracking-widest text-xs">{insights.advisory_title}:</span>
            <span>{insights.stuck_count > 0 ? `${insights.stuck_count} developers are currently stuck awaiting onboarding.` : 'All developers are progressing normally.'}</span>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* CHART 1: Topic Distribution (Donut) */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-6 border-b border-[#E5E0D8] pb-2">AI Conversational Topic Distribution</h2>
          <div className="h-64">
            {topicData.length > 0 ? (
              <ResponsiveContainer height="100%" width="100%">
                <PieChart>
                  <Pie data={topicData} cx="50%" cy="50%" dataKey="value" innerRadius={70} outerRadius={90} paddingAngle={2} stroke="none">
                    {topicData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs font-mono text-[#7A756D]">
                No query data available.
              </div>
            )}
          </div>
          {/* Legend */}
          <div className="mt-4 grid grid-cols-2 gap-2">
            {topicData.map((entry, idx) => (
              <div key={idx} className="flex items-center text-xs font-mono text-[#7A756D]">
                <div className="w-2 h-2 mr-2" style={{ backgroundColor: COLORS[idx % COLORS.length] }}></div>
                {entry.name}: {entry.value}%
              </div>
            ))}
          </div>
        </div>

        {/* CHART 2: Developer Progress Distribution (Bar) */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-6 border-b border-[#E5E0D8] pb-2">Cohort Progress Tracker</h2>
          <div className="h-64 mt-4">
            {devData.length > 0 ? (
              <ResponsiveContainer height="100%" width="100%">
                <BarChart data={devData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <RechartsTooltip cursor={{ fill: '#FBF9F5' }} content={<CustomTooltip />} />
                  <Bar dataKey="progress" fill="#1A1A1A" maxBarSize={40} radius={[2, 2, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs font-mono text-[#7A756D]">
                No developer data available.
              </div>
            )}
          </div>
        </div>

      </div>

      {/* ADVANCED CHARTS GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        
        {/* Frustration Index (BarChart) */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-6 border-b border-[#E5E0D8] pb-2">Developer Frustration Index</h2>
          <div className="h-64 mt-4">
            {advancedData && advancedData.frustration_index.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={advancedData.frustration_index} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <RechartsTooltip cursor={{ fill: '#FBF9F5' }} content={<CustomTooltip />} />
                  <Bar dataKey="score" fill="#1A1A1A" maxBarSize={40} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs font-mono text-[#7A756D]">No data available.</div>
            )}
          </div>
        </div>

        {/* Autonomy vs. AI Reliance (RadarChart) */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-6 border-b border-[#E5E0D8] pb-2">Autonomy vs. AI Reliance</h2>
          <div className="h-64 mt-4">
            {advancedData && advancedData.autonomy_radar.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart outerRadius="80%" data={advancedData.autonomy_radar}>
                  <PolarGrid stroke="#E5E0D8" />
                  <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <PolarRadiusAxis angle={30} domain={[0, 10]} tick={false} axisLine={false} />
                  <Radar name="Autonomy" dataKey="autonomy" stroke="#1A1A1A" fill="#C2DFE3" fillOpacity={0.6} />
                  <Radar name="Reliance" dataKey="reliance" stroke="#5C6B73" fill="#9DB4C0" fillOpacity={0.6} />
                  <RechartsTooltip content={<CustomTooltip />} />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs font-mono text-[#7A756D]">No data available.</div>
            )}
          </div>
        </div>

        {/* Developer Proficiency Matrix (ScatterChart) */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-6 border-b border-[#E5E0D8] pb-2">Developer Proficiency Matrix</h2>
          <div className="h-64 mt-4">
            {advancedData && advancedData.proficiency_matrix.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" />
                  <XAxis dataKey="progress" type="number" name="Progress" domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <YAxis dataKey="depth" type="number" name="Tech Depth" domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <ZAxis dataKey="name" type="category" name="Developer" />
                  <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
                  <Scatter name="Developers" data={advancedData.proficiency_matrix} fill="#E0A96D" />
                </ScatterChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs font-mono text-[#7A756D]">No data available.</div>
            )}
          </div>
        </div>

        {/* Task Velocity (LineChart) */}
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-6 border-b border-[#E5E0D8] pb-2">Task Velocity (Avg Hours)</h2>
          <div className="h-64 mt-4">
             {advancedData && advancedData.task_velocity.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={advancedData.task_velocity} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid stroke="#E5E0D8" strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#7A756D' }} />
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Line type="monotone" dataKey="hours" stroke="#1A1A1A" strokeWidth={2} dot={{ fill: '#1A1A1A', r: 4 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
             ) : (
              <div className="h-full flex items-center justify-center text-xs font-mono text-[#7A756D]">No data available.</div>
             )}
          </div>
        </div>

      </div>

      {/* AI Insight Text Box */}
      {insights && (
        <div className="border border-[#E5E0D8] bg-[#FFFFFF] p-6 mt-6 rounded-none shadow-none">
          <h2 className="text-sm font-serif mb-4 flex items-center">
            <span className="w-2 h-2 bg-[#1A1A1A] mr-2"></span>
            Synthesized AI Insight
          </h2>
          <p className="text-sm font-sans text-[#1A1A1A] leading-relaxed">
            {insights.ai_insight}
          </p>
        </div>
      )}

    </div>
  );
};
