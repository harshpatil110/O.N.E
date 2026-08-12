# Nexus AI Innovations — O.N.E. Platform Architecture Overview

## System Purpose
The **O.N.E. (Onboarding Navigation Environment)** platform is an
AI-powered multi-agent system that guides new employees through their
complete onboarding journey at Nexus AI Innovations.

## High-Level Architecture
```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  React UI   │────▶│  FastAPI      │────▶│  PostgreSQL     │
│  (Vite)     │     │  Backend      │     │  (Supabase)     │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
                ┌──────────┴──────────┐
                │   Hermes Agent      │
                │   (Supervisor)      │
                ├─────────┬───────────┤
                │         │           │
           ┌────▼──┐ ┌───▼───┐ ┌─────▼────┐
           │ RAG   │ │ Jira  │ │ GitHub   │
           │ Agent │ │ MCP   │ │ MCP      │
           └───┬───┘ └───────┘ └──────────┘
               │
          ┌────▼────┐
          │ChromaDB │
          │(Vectors)│
          └─────────┘
```

## Core Components
1. **Frontend:** React 18 + Vite + Tailwind CSS.
2. **Backend:** Python 3.12 + FastAPI + SQLAlchemy ORM.
3. **Database:** PostgreSQL hosted on Supabase.
4. **Cache:** Redis for session state and rate limiting.
5. **AI Layer:** LangChain orchestration → Ollama local LLMs.
6. **Vector Store:** ChromaDB for RAG document embeddings.
7. **Agent Router:** Hermes Agent (Supervisor pattern) dispatches
   sub-agents for specific tasks.
8. **External Integrations:** Jira Cloud (MCP), GitHub (MCP + PAT).

## Data Flow
1. User sends a chat message from the React frontend.
2. FastAPI receives the request and authenticates via JWT.
3. The `AgentOrchestrator` invokes the Hermes Supervisor.
4. Hermes routes to the appropriate sub-agent (RAG, Jira, GitHub).
5. Sub-agents execute tools and return structured responses.
6. Response is streamed back to the frontend via the chat API.

---
*Architecture maintained by Harshvardhan Patil*
