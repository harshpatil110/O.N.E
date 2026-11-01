<div align="center">

---

## 📌 Overview

Traditional engineering onboarding relies on stale wikis, fragmented Slack threads, and manual environment checks. **O.N.E. (Onboarding Navigation Environment)** replaces static checklists with an active, stateful AI mentor and workspace orchestrator.

When a new engineer logs into the O.N.E. Console (whether as a `Backend Dev`, `Frontend Dev`, `AI Dev`, or `Database Dev`), O.N.E. dynamically tracks their onboarding curriculum in real time. Using a **Dual-Agent Architecture**, O.N.E. pairs a local, privacy-first **LangGraph + Ollama (`qwen3:4b`)** reasoning core with a dedicated **Hermes MCP Gateway**—allowing developers to query live **Notion** databases, check **Vercel** deployment logs, inspect **Slack** channels, and verify **Jira / Confluence** tickets directly from a single unified console.

---

## 🏗️ System Architecture & Multi-Agent Topology

O.N.E. separates **conversational state & task verification** (handled locally on GPU via Ollama) from **external workspace I/O** (delegated via the Hermes Agent MCP Server on port `8642`).

```text
# O.N.E. — Onboarding Navigation Environment
> **Autonomous Multi-Agent Developer Onboarding & Workspace Orchestration Platform**

![React](https://img.shields.io/badge/Frontend-React_18_%2B_Vite-111111?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF6F00?style=flat-square)
![Ollama](https://img.shields.io/badge/Local_LLM-Qwen3_4B_(Ollama)-000000?style=flat-square)
![Hermes MCP](https://img.shields.io/badge/MCP_Gateway-Hermes_Agent_(:8642)-6E56CF?style=flat-square)
![Supabase](https://img.shields.io/badge/Database-Supabase_PostgreSQL-3ECF8E?style=flat-square&logo=supabase)

---

## 1. Executive Overview
**O.N.E. (Onboarding Navigation Environment)** is an enterprise-grade, agentic AI developer onboarding ecosystem designed to eliminate first-week engineering friction. Instead of handing new hires static wiki links and outdated setup docs, O.N.E. pairs every developer with a stateful, database-grounded **LangGraph AI Mentor** connected directly to live engineering tools (**Notion, Slack, Vercel, Jira, Confluence, and Git**) via the **Hermes Model Context Protocol (MCP) Gateway**.

Built with a **Warm Editorial Minimalism** aesthetic (`#F7F5F0` off-white canvas, high-contrast typography, flat structural cards, and generous whitespace), O.N.E. guides engineers step-by-step through role-specific tasks, verifies terminal/Git/API milestones in real time, and updates an executive Admin Console automatically.

---

## 2. Unique Architectural Elements (What Sets O.N.E. Apart)

### 🧠 1. Dual-Brain Hybrid Agentic Architecture (Local Edge + Cloud MCP Engine)
* **Primary Conversational & Task Engine (Local Edge Privacy):** Powered by **LangGraph** and local **Ollama (`qwen3:4b`)** on port `11434` with `keep_alive="-1"` VRAM pinning and automatic Regex `<think>` tag sanitization (`re.sub(r'<think>.*?</think>', '', text)`) for zero cold-start lag.
* **External MCP Execution Engine (Hermes Agent Gateway on Port `8642`):** Offloads complex multi-step JSON-RPC tool schemas to high-speed inference (**Nous Portal `:Free` / Groq `llama-3.3-70b-versatile`**) via the `delegate_to_hermes` bridge. This prevents local GPU queueing while enforcing bounded fetching (1–2 tool rounds, 4,096 max tokens) and automated Markdown structure normalization (`format_hermes_markdown`).

### 📌 2. Just-In-Time (JIT) Database-Grounded Task Injection
* Rather than relying on fragile prompt history, O.N.E. queries `developer_task_state` in **Supabase PostgreSQL** on *every incoming chat turn* and injects the developer's exact active task (e.g., `Test API Endpoints using Swagger Docs (/docs)`) directly into the LangGraph execution node.
* Prevents the LLM from summarizing away external tool outputs, preserving 100% of structured records returned by the Hermes MCP gateway.

### 🔐 3. Dual-Sync Supabase Auth & Row-Level Security (RLS)
* Synchronizes `auth.users` and `auth.identities` with `public.users` using deterministic UUID & bcrypt hash preservation alongside a PostgreSQL `SECURITY DEFINER` trigger (`on_auth_user_created`).
* Configured over **Supavisor IPv4 Session Pooler** (`aws-0-ap-southeast-1.pooler.supabase.com:5432`) with `pool_pre_ping=True` and built-in multi-stage DNS/socket diagnostics (`scripts/diagnose_db.py`).

### 🎯 4. Role-Aware Departmental Tracks & Live Verification
* Tailors onboarding tracks dynamically based on `department_role` (`backend dev`, `frontend dev`, `ai dev`, `database dev`, `admin`), complete with automated task state progression (`mark_task_complete`), internal RAG documentation lookup, and deduplicated conversation persistence (`conversation_logs`).

---

## 3. System Architecture & Data Flow

```text
+-----------------------------------------------------------------------------------+
|                        O.N.E. FRONTEND (React + Vite :5173)                       |
|   Warm Editorial Minimalist UI (#F7F5F0) | Role Console | Workspace Context Chip  |
+-----------------------------------------+-----------------------------------------+
                                          | REST / JWT Auth
                                          v
+-----------------------------------------------------------------------------------+
|                        O.N.E. BACKEND (FastAPI :8000)                             |
|   JIT Task State Injector | Message Deduplication | Regex <think> Sanitizer       |
+-------------------+-----------------------------+---------------------------------+
                    |                             |
                    | SQLAlchemy Pooler (:5432)   | LangGraph Orchestrator
                    v                             v
+-----------------------------------+   +-------------------------------------------+
|   SUPABASE POSTGRESQL (ap-se-1)   |   |     LANGGRAPH AGENT NODE (:11434)         |
| - auth.users & auth.identities    |   | - Local Ollama: qwen3:4b (keep_alive=-1)  |
| - public.users (RLS Protected)    |   | - Tools:                                  |
| - developer_task_state            |   |   1. mark_task_complete                   |
| - conversation_logs               |   |   2. search_onboarding_docs (RAG)         |
+-----------------------------------+   |   3. delegate_to_hermes (MCP Bridge)      |
                                        +---------------------+---------------------+
                                                              | HTTP POST (:8642)
                                                              v
                                        +-------------------------------------------+
                                        |     HERMES MCP GATEWAY (:8642)            |
                                        | - Bounded Fetching (Max 1-2 Tool Rounds)  |
                                        | - Markdown Formatter (format_hermes_md)   |
                                        | - Connected MCP Servers:                  |
                                        |   * Notion (Databases, Pages, To-Dos)     |
                                        |   * Vercel (Deployments, Build Logs)      |
                                        |   * Slack (Channels, Messages)            |
                                        |   * Jira & Confluence (Tickets, Docs)     |
                                        +-------------------------------------------+
4. Complete Feature Matrix
Feature Module	Description
Stateful Onboarding Mentor	Context-aware chat assistant grounded in the developer's role, completed milestones, and current active task on every turn.
Hermes MCP Workspace Bridge	Live read/write orchestration across Notion, Vercel, Slack, Jira, and Confluence rendered inside dedicated WORKSPACE CONTEXT (HERMES) UI cards.
RAG Knowledge Base	Semantic search across internal architecture decision records (ADRs), environment guides, and engineering standards.
Automated Task Progression	Evaluates developer verification outputs and transitions tasks from pending -> in_progress -> completed automatically.
Admin & Engineering Console	Real-time visibility into cohort onboarding progress, task bottlenecks, and conversation audit logs.
Self-Healing DB Diagnostics	Built-in scripts/diagnose_db.py script that tests IPv4/IPv6 getaddrinfo() DNS resolution, port 5432 socket handshakes, and SQLAlchemy sessions.
5. Repository Structure
Plaintext
ONE/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── langgraph_agent.py      # LangGraph state machine, JIT task injection & post-tool routing
│   │   │   ├── hermes_tool.py          # delegate_to_hermes MCP bridge & Markdown post-processor
│   │   │   ├── task_tools.py           # Onboarding task verification & completion tools
│   │   │   └── rag_tool.py             # Internal documentation Retrieval-Augmented Generation tool
│   │   ├── models.py                   # SQLAlchemy ORM models (Users, DeveloperTaskState, ConversationLog)
│   │   ├── database.py                 # Supavisor Session Pooler engine with pool_pre_ping=True
│   │   ├── config.py                   # Centralized environment & model settings
│   │   └── main.py                     # FastAPI application entry point & CORS/auth routes
│   ├── scripts/
│   │   ├── diagnose_db.py              # Multi-stage DNS, TCP socket & SQLAlchemy diagnostic utility
│   │   └── supabase_auth_sync.py       # Idempotent auth.users <-> public.users migration & RLS script
│   ├── .env                            # Backend environment configuration
│   └── requirements.txt                # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/                 # Warm Editorial Minimalist UI components & Workspace Context chips
│   │   ├── pages/                      # Sign-In Console, Developer Workspace & Admin Dashboard
│   │   ├── services/
│   │   │   └── api.js                  # Axios client configured with 180s timeout for MCP tool execution
│   │   └── App.jsx                     # Frontend router & session state management
│   ├── package.json
│   └── vite.config.js
└── README.md
6. Prerequisites
Ensure the following are installed on your local machine (Windows 10/11, macOS, or Linux):

Python 3.11+ (with venv)

Node.js 18+ & npm

Ollama (running locally on port 11434 — ollama.com)

Hermes Agent CLI (hermes installed for MCP Gateway orchestration on port 8642)

Supabase Project (PostgreSQL database with Session Pooler enabled)

7. Step-by-Step Setup & Installation
Step 1: Clone the Repository
PowerShell
git clone [https://github.com/your-username/ONE.git](https://github.com/your-username/ONE.git)
cd ONE
Step 2: Pull & Verify the Local Ollama Model (qwen3:4b)
PowerShell
ollama pull qwen3:4b
ollama list
Step 3: Set Up the Python Backend & .env
PowerShell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
Create backend/.env with the following variables (using the Supabase IPv4 Session Pooler URL):

Code snippet
# Supabase PostgreSQL (IPv4 Session Pooler - Singapore ap-southeast-1)
DATABASE_URL=postgresql://postgres.skvdtmbujkfqwopjnnqg:[YOUR_DB_PASSWORD]@[aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require](https://aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require)

# Supabase API Keys
SUPABASE_URL=[https://skvdtmbujkfqwopjnnqg.supabase.co](https://skvdtmbujkfqwopjnnqg.supabase.co)
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Local LangGraph LLM (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b

# Hermes Agent MCP Gateway
HERMES_API_URL=http://localhost:8642/v1/chat/completions
HERMES_API_KEY=hermes-local-key
HERMES_MAX_TOKENS=4096

# JWT & Application Security
JWT_SECRET_KEY=your_super_secret_jwt_key
Step 4: Verify Database Connection & Sync Supabase Auth
Run the diagnostic script to verify IPv4 DNS resolution, port 5432 TCP connection, and SQLAlchemy readiness:

PowerShell
.\venv\Scripts\python scripts\diagnose_db.py
To sync public.users into auth.users / auth.identities and apply Row-Level Security (RLS) policies:

PowerShell
.\venv\Scripts\python scripts\supabase_auth_sync.py
Step 5: Configure the Hermes MCP Gateway (Port 8642)
Enable the HTTP API server on port 8642 and configure your fast cloud provider (Nous Portal or Groq) so multi-step MCP tools execute in seconds:

Option A — Using Nous Portal (Free Built-In Cloud):

PowerShell
hermes config set API_SERVER_ENABLED true
hermes config set API_SERVER_KEY hermes-local-key
hermes config set model.max_tokens 4096
hermes setup --portal
hermes model
# Select Nous Portal -> Choose "Step 3.7 Flash:Free" or "Solar Mini4:Free"
Option B — Using Groq LPU (llama-3.3-70b-versatile):

PowerShell
hermes config set API_SERVER_ENABLED true
hermes config set API_SERVER_KEY hermes-local-key
hermes config set model.provider "custom"
hermes config set model.base_url "[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1)"
hermes config set model.default "llama-3.3-70b-versatile"
hermes config set model.max_tokens 4096
hermes config set OPENAI_API_KEY "gsk_your_groq_api_key_here"
hermes config set CUSTOM_API_KEY "gsk_your_groq_api_key_here"
Step 6: Install Frontend Dependencies
PowerShell
cd ..\frontend
npm install
8. How to Run All Services (Full Stack Execution)
Open 4 terminals (or run Ollama and Hermes as background services) to launch the full platform:

Terminal 1 — Local Ollama Server (Port 11434)
(Skip if Ollama is already running in your Windows system tray)

PowerShell
ollama serve
Terminal 2 — Hermes MCP Gateway (Port 8642)
Run in the foreground to watch live MCP tool execution logs (or run hermes gateway start for background daemon mode):

PowerShell
hermes gateway stop
hermes gateway
Health Check URL: http://localhost:8642/health -> returns {"status": "ok"}

Terminal 3 — FastAPI Backend Server (Port 8000)
PowerShell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Interactive Swagger Docs: http://localhost:8000/docs

Terminal 4 — React + Vite Frontend (Port 5173)
PowerShell
cd frontend
npm run dev
O.N.E. Web Console: http://localhost:5173

9. Seeded Workspace Accounts & Test Queries
Default Accounts
Name	Email	Role	Department Track
Master Admin	patilha2005@gmail.com	admin	Platform Administrator
Harsh Patil	harsh123@gmail.com	employee	ai dev
Manas Patil	manas123@gmail.com	employee	backend dev
Archit Chitte	archit123@gmail.com	employee	frontend dev
Parth Narkar	parth123@gmail.com	employee	database dev
Sample Prompts to Test in the Chat Console
Notion MCP Integration: "Can you see my Notion and tell me what databases, pages, and tasks I currently have?"

Vercel MCP Integration: "What are my recent Vercel deployment statuses?"

Slack MCP Integration: "What are my latest Slack messages?"

Task Completion Verification: "I have finished testing the API endpoints in Swagger Docs (/docs). Please mark this task as complete."

10. Troubleshooting Guide
ERR_CONNECTION_REFUSED on http://localhost:8642/health:
The background gateway process started before API_SERVER_ENABLED was set. Force-restart port 8642:

PowerShell
hermes config set API_SERVER_ENABLED true
hermes gateway stop
Get-NetTCPConnection -LocalPort 8642 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
hermes gateway
Cannot resolve host db.<project-ref>.supabase.co:
Supabase Direct Connections are IPv6-only on the Free tier. Update DATABASE_URL in backend/.env to use the Supavisor IPv4 Session Pooler (aws-0-ap-southeast-1.pooler.supabase.com:5432 with username postgres.<project-ref>).

Read timed out on Port 8642 during Vercel/Slack Queries:
Run hermes config show and verify base_url is not pointing to http://localhost:11434/v1 (which causes a single-GPU bottleneck alongside LangGraph). Point Hermes to Nous Portal (Step 3.7 Flash:Free) or Groq (llama-3.3-70b-versatile).

11. Author
Harshvardhan Patil

B.E. in Information Technology — Vivekanand Education Society's Institute of Technology (VESIT), Mumbai

BS in Data Science & Applications — Indian Institute of Technology (IIT) Madras

Portfolio: harsh-portfolio.xyz
```
