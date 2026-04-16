import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Search, Terminal, FileCode2, ShieldAlert, Cpu, ArrowRight, X, LayoutDashboard, MessageSquare, ListChecks, BookOpen, Code } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export const KnowledgeBasePage = () => {
    const { user } = useAuth();
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedDoc, setSelectedDoc] = useState(null);
    const [docContent, setDocContent] = useState('');
    const [loadingDoc, setLoadingDoc] = useState(false);

    useEffect(() => {
        const fetchDocs = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/docs', {
                    withCredentials: true
                });
                setCategories(response.data);
            } catch (err) {
                console.error("Failed to fetch docs", err);
            } finally {
                setLoading(false);
            }
        };
        fetchDocs();
    }, []);

    const handleOpenDoc = async (doc) => {
        setSelectedDoc(doc);
        setLoadingDoc(true);
        try {
            const response = await axios.get(`http://localhost:8000/api/v1/docs/${doc.filename}`, {
                withCredentials: true
            });
            setDocContent(response.data);
        } catch (err) {
            console.error("Failed to fetch doc content", err);
            setDocContent("Failed to load document content. Please try again.");
        } finally {
            setLoadingDoc(false);
        }
    };

    const handleCloseDoc = () => {
        setSelectedDoc(null);
        setDocContent('');
    };

    const filteredCategories = categories.map(cat => {
        const filteredArticles = cat.articles.filter(article => 
            article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            article.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
        );
        return {
            ...cat,
            articles: filteredArticles
        };
    }).filter(cat => cat.articles.length > 0);

    const getIcon = (category) => {
        switch(category) {
            case 'Setup Guides': return <Terminal size={20} className="text-emerald-400" />;
            case 'Architecture': return <Cpu size={20} className="text-[#4c6ef5]" />;
            case 'Troubleshooting': return <ShieldAlert size={20} className="text-rose-400" />;
            default: return <FileCode2 size={20} className="text-indigo-400" />;
        }
    };

    // Keep Sidebar identical to Developer Dashboard to fulfill identical layout flow
    const Sidebar = () => (
        <aside className="w-64 bg-[#111114] border-r border-[#1f1f23] flex flex-col z-10 hidden md:flex h-full flex-shrink-0">
          <div className="h-16 px-6 flex items-center border-b border-[#1f1f23] bg-transparent">
            <div className="flex items-center gap-2.5">
              <div className="size-7 bg-[#4c6ef5] rounded flex items-center justify-center text-white shadow-lg shadow-[#4c6ef5]/20">
                <span className="font-bold font-mono text-sm tracking-tighter">O.</span>
              </div>
              <h2 className="text-white text-lg font-extrabold tracking-tight">O.N.E</h2>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-6 scrollbar-hide">
            <div className="space-y-1">
              <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-2 mb-3">Onboarding Nav</h3>
              
              <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm group">
                <LayoutDashboard size={18} />
                Dashboard
              </Link>
              
              <Link to="/chat" className="flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
                <MessageSquare size={18} />
                Chat Assistant
              </Link>
               
              <Link to="#" className="flex items-center gap-3 px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
                <ListChecks size={18} />
                Checklist
              </Link>
               
              <Link to="/docs" className="flex items-center gap-3 px-3 py-2 bg-[#4c6ef5]/10 text-[#4c6ef5] rounded-xl transition-colors font-medium text-sm group">
                <BookOpen size={18} />
                Docs
              </Link>
            </div>

            <div className="mt-auto space-y-3 pb-2">
              <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-2 mb-3">Integrations</h3>
               <button className="flex items-center gap-3 px-3 py-2 w-full text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
                <Code size={16} /> GitHub
              </button>
               <button className="flex items-center gap-3 px-3 py-2 w-full text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-xl transition-colors font-medium text-sm">
                <MessageSquare size={16} /> Slack
              </button>
            </div>
          </div>
        </aside>
    );

    return (
        <div className="flex h-screen bg-[#0a0a0c] text-white overflow-hidden font-sans selection:bg-[#4c6ef5]/30 relative">
            <div 
                className="absolute inset-0 z-0 pointer-events-none opacity-40 mix-blend-screen"
                style={{
                  backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0)',
                  backgroundSize: '24px 24px'
                }}
            />
            
            <Sidebar />

            <main className="flex-1 overflow-y-auto z-10 relative">
                {selectedDoc ? (
                    <div className="absolute inset-0 bg-[#0a0a0c] z-50 flex flex-col overflow-hidden">
                        <div className="h-16 px-6 lg:px-12 flex items-center justify-between border-b border-[#1f1f23] bg-[#111114]/50 backdrop-blur-md sticky top-0 z-10">
                            <div className="flex items-center gap-4">
                                <button onClick={handleCloseDoc} className="size-8 flex items-center justify-center rounded-lg bg-white/5 text-slate-400 border border-white/10 hover:bg-[#4c6ef5]/10 hover:text-[#4c6ef5] hover:border-[#4c6ef5]/20 transition-all">
                                    <X size={18} />
                                </button>
                                <span className="text-sm font-bold tracking-tight text-white">{selectedDoc.title}</span>
                            </div>
                        </div>
                        <div className="flex-1 overflow-y-auto p-6 lg:p-12 scrollbar-hide">
                            <div className="max-w-3xl mx-auto">
                                {loadingDoc ? (
                                    <div className="animate-pulse space-y-4">
                                        <div className="h-8 bg-white/5 rounded-lg w-1/3 mb-8"></div>
                                        <div className="h-4 bg-white/5 rounded w-full"></div>
                                        <div className="h-4 bg-white/5 rounded w-5/6"></div>
                                        <div className="h-4 bg-white/5 rounded w-4/6"></div>
                                    </div>
                                ) : (
                                    <div className="prose prose-invert prose-slate max-w-none prose-headings:text-white prose-a:text-[#4c6ef5] prose-pre:bg-[#111114] prose-pre:border prose-pre:border-[#1f1f23] prose-code:text-[#4c6ef5] prose-p:text-slate-400 prose-ul:text-slate-400 marker:text-[#4c6ef5] prose-strong:text-white">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {docContent}
                                        </ReactMarkdown>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="p-6 md:p-10 lg:p-12 max-w-[1400px] mx-auto">
                        <header className="mb-12">
                            <h1 className="text-4xl font-extrabold tracking-tight text-white mb-4">
                                Knowledge Base
                            </h1>
                            <p className="text-base text-slate-400 max-w-xl font-medium">
                                Explore our comprehensive guides, technical snippets, and powerful tools to help you build faster with O.N.E.
                            </p>
                            
                            <div className="mt-8 relative max-w-2xl">
                                <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-[#4c6ef5]" size={18} />
                                <input 
                                    type="text" 
                                    placeholder="Search documentation... (CMD + K)" 
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full bg-[#111114]/80 border border-[#1f1f23] text-white placeholder-slate-500 font-medium rounded-xl pl-12 pr-4 py-4 outline-none focus:border-[#4c6ef5]/50 focus:ring-4 focus:ring-[#4c6ef5]/10 transition-all backdrop-blur-sm shadow-xl"
                                />
                            </div>
                        </header>

                        {loading ? (
                             <div className="p-12 text-center text-slate-500 text-xs tracking-widest uppercase font-bold animate-pulse bg-[#111114]/20 rounded-2xl border border-[#1f1f23]">Scanning Knowledge Base Data...</div>
                        ) : filteredCategories.length === 0 ? (
                            <div className="p-12 text-center text-slate-500 bg-[#111114]/20 rounded-2xl border border-[#1f1f23] font-medium tracking-tight">No documents found matching your search. Try different keywords.</div>
                        ) : (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                                {filteredCategories.map((category) => (
                                    <div key={category.category} className="space-y-6">
                                        <div className="flex items-center gap-3 border-b border-[#1f1f23] pb-3">
                                            {getIcon(category.category)}
                                            <h2 className="text-lg font-bold text-white tracking-tight">{category.category}</h2>
                                        </div>
                                        
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                            {category.articles.map(article => (
                                                <div 
                                                    key={article.id} 
                                                    onClick={() => handleOpenDoc(article)}
                                                    className="bg-[#111114]/40 border border-[#1f1f23] rounded-xl p-5 hover:border-[#4c6ef5]/30 hover:bg-[#111114] transition-all cursor-pointer group flex flex-col justify-between min-h-[140px] shadow-sm relative overflow-hidden"
                                                >
                                                    <div className="absolute inset-0 bg-gradient-to-br from-[#4c6ef5]/0 to-[#4c6ef5]/0 group-hover:to-[#4c6ef5]/[0.02] pointer-events-none transition-colors" />
                                                    <div className="relative z-10">
                                                        <h3 className="text-sm font-bold text-slate-200 group-hover:text-[#4c6ef5] transition-colors mb-2 leading-snug">
                                                            {article.title}
                                                        </h3>
                                                        <p className="text-[11px] font-medium text-slate-500 line-clamp-2 leading-relaxed">
                                                            {article.excerpt || "No excerpt provided."}
                                                        </p>
                                                    </div>
                                                    <div className="mt-4 flex items-center text-[10px] font-bold uppercase tracking-widest text-slate-600 group-hover:text-[#4c6ef5] transition-colors gap-1 relative z-10">
                                                        Read Docs <ArrowRight size={12} className="relative group-hover:translate-x-0.5 transition-transform" />
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
};
