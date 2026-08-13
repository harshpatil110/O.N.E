import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Search, Terminal, FileCode2, ShieldAlert, Cpu, ArrowRight, X, LayoutDashboard, MessageSquare, ListChecks, BookOpen, Code } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export const KnowledgeBasePage = () => {
    // eslint-disable-next-line no-unused-vars
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
            case 'Setup Guides': return <Terminal size={18} className="text-stone-700" />;
            case 'Architecture': return <Cpu size={18} className="text-blue-800" />;
            case 'Troubleshooting': return <ShieldAlert size={18} className="text-rose-700" />;
            default: return <FileCode2 size={18} className="text-stone-700" />;
        }
    };



    return (
        <div className="flex h-full bg-[#F7F5F0] text-stone-900 overflow-hidden font-sans selection:bg-blue-100 relative">
            <div 
                className="absolute inset-0 z-0 pointer-events-none opacity-40"
                style={{
                  backgroundImage: 'radial-gradient(circle at 1px 1px, #E7E5E4 1px, transparent 0)',
                  backgroundSize: '20px 20px'
                }}
            />
            


            <main className="flex-1 overflow-y-auto z-10 relative">
                {selectedDoc ? (
                    <div className="absolute inset-0 bg-[#F7F5F0] z-50 flex flex-col overflow-hidden">
                        <div className="h-16 px-6 lg:px-12 flex items-center justify-between border-b border-stone-200 bg-white sticky top-0 z-10">
                            <div className="flex items-center gap-4">
                                <button onClick={handleCloseDoc} className="size-7 flex items-center justify-center rounded-sm bg-stone-100 text-stone-700 border border-stone-200 hover:bg-stone-900 hover:text-white transition-colors">
                                    <X size={16} />
                                </button>
                                <span className="text-sm font-serif font-bold text-stone-900">{selectedDoc.title}</span>
                            </div>
                        </div>
                        <div className="flex-1 overflow-y-auto p-6 lg:p-12">
                            <div className="max-w-3xl mx-auto bg-white border border-stone-200 p-8 rounded-md shadow-sm">
                                {loadingDoc ? (
                                    <div className="animate-pulse space-y-4">
                                        <div className="h-6 bg-stone-100 rounded w-1/3 mb-6"></div>
                                        <div className="h-3 bg-stone-100 rounded w-full"></div>
                                        <div className="h-3 bg-stone-100 rounded w-5/6"></div>
                                    </div>
                                ) : (
                                    <div className="prose prose-stone max-w-none prose-headings:font-serif prose-headings:text-stone-900 prose-a:text-blue-800 prose-pre:bg-stone-100 prose-pre:border prose-pre:border-stone-200 prose-code:font-mono prose-code:text-stone-800">
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
                        <header className="mb-10">
                            <h1 className="text-3xl font-serif font-bold tracking-tight text-stone-900 mb-2">
                                Knowledge Base
                            </h1>
                            <p className="text-xs font-mono uppercase tracking-widest text-stone-500 max-w-xl">
                                Architectural reference, setup guides, and system documentation.
                            </p>
                            
                            <div className="mt-6 relative max-w-xl">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" size={16} />
                                <input 
                                    type="text" 
                                    placeholder="Search documentation..." 
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full bg-white border border-stone-300 text-stone-900 placeholder:text-stone-400 font-medium rounded-md pl-10 pr-4 py-3 outline-none focus:border-stone-900 transition-colors shadow-sm text-xs"
                                />
                            </div>
                        </header>

                        {loading ? (
                             <div className="p-12 text-center text-stone-400 font-mono text-xs tracking-widest uppercase animate-pulse bg-white rounded-md border border-stone-200">Scanning Knowledge Base Data...</div>
                        ) : filteredCategories.length === 0 ? (
                            <div className="p-12 text-center text-stone-400 font-mono text-xs bg-white rounded-md border border-stone-200">No documents found matching your search.</div>
                        ) : (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {filteredCategories.map((category) => (
                                    <div key={category.category} className="space-y-4">
                                        <div className="flex items-center gap-2.5 border-b border-stone-200 pb-2">
                                            {getIcon(category.category)}
                                            <h2 className="text-base font-serif font-bold text-stone-900 tracking-tight">{category.category}</h2>
                                        </div>
                                        
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                            {category.articles.map(article => (
                                                <div 
                                                    key={article.id} 
                                                    onClick={() => handleOpenDoc(article)}
                                                    className="bg-white border border-stone-200 rounded-md p-5 hover:border-stone-900 transition-colors cursor-pointer group flex flex-col justify-between min-h-[130px] shadow-sm relative"
                                                >
                                                    <div>
                                                        <h3 className="text-xs font-bold text-stone-900 group-hover:text-blue-800 transition-colors mb-1.5 leading-snug">
                                                            {article.title}
                                                        </h3>
                                                        <p className="text-[11px] text-stone-500 font-mono line-clamp-2 leading-relaxed">
                                                            {article.excerpt || "No excerpt provided."}
                                                        </p>
                                                    </div>
                                                    <div className="mt-4 flex items-center text-[10px] font-mono font-bold uppercase tracking-widest text-stone-400 group-hover:text-stone-900 transition-colors gap-1">
                                                        Read <ArrowRight size={10} className="relative group-hover:translate-x-0.5 transition-transform" />
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
