<div align="center">

# 🚀 O.N.E. — Onboarding Navigation Environment

### _Enterprise-Grade Agentic AI Developer Onboarding Platform_

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct_Agent-FF6B35?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Ollama](https://img.shields.io/badge/Ollama-qwen3:4b-000000?style=for-the-badge&logo=ollama)](https://ollama.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Hermes](https://img.shields.io/badge/Hermes_Agent-MCP_Gateway-8B5CF6?style=for-the-badge)](https://github.com/NousResearch/hermes-agent)

**O.N.E.** automates and guides new software engineers through their entire company onboarding — from environment setup and codebase orientation to task management, documentation search, and live workspace interactions — all powered by a locally-hosted LangGraph ReAct agent with multi-tool orchestration.

</div>

---

## 📑 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Core Features](#-core-features)
- [Agent Tools & Capabilities](#-agent-tools--capabilities)
- [Technology Stack](#-technology-stack)
- [Directory Structure](#-directory-structure)
- [Prerequisites](#-prerequisites)
- [Environment Variables](#-environment-variables)
- [Step-by-Step Setup](#-step-by-step-setup)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🏗 Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                        │
│  LoginPage → DeveloperOnboardingHub → ChatPage → ChecklistPage → ... │
│                 Axios (180s timeout) → http://localhost:8000           │
└────────────────────────────────┬──────────────────────────────────────┘
                                 │ REST API (CORS-enabled)
                                 ▼
┌───────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI + LangGraph)                       │
│                                                                       │
│  ┌─────────────┐   ┌───────────────────────────────────────────────┐  │
│  │  API Routes  │   │          LangGraph ReAct Agent                │  │
│  │ /api/v1/*    │──▶│  supervisor → intent_router → tool_node       │  │
│  │  - auth      │   │                                               │  │
│  │  - chat      │   │  Tools:                                       │  │
│  │  - tasks     │   │   ├─ get_current_task                         │  │
│  │  - checklist │   │   ├─ mark_task_complete (LLM-verified)        │  │
│  │  - onboarding│   │   ├─ delegate_to_hermes (MCP Gateway)         │  │
│  │  - docs      │   │   ├─ search_corporate_knowledge (RAG)         │  │
│  │  - analytics │   │   ├─ get_open_pull_requests                   │  │
│  │  - admin     │   │   ├─ get_recent_commits                       │  │
│  │              │   │   └─ get_repository_issues                    │  │
│  └─────────────┘   └──────────┬────────────────────────────────────┘  │
│                                │                                       │
│  ┌─────────────────────────────┼───────────────────────────────────┐  │
│  │              LLM Layer      │                                   │  │
│  │  ┌───────────────┐    ┌─────▼──────┐    ┌──────────────────┐   │  │
│  │  │ Ollama (Local) │    │ ChromaDB   │    │ Hermes Agent     │   │  │
│  │  │ qwen3:4b       │    │ RAG Vector │    │ MCP Gateway      │   │  │
│  │  │ :11434         │    │ Store      │    │ :8642            │   │  │
│  │  └───────────────┘    └────────────┘    │ ┌──────────────┐ │   │  │
│  │                                          │ │ Slack        │ │   │  │
│  │                                          │ │ Notion       │ │   │  │
│  │                                          │ │ Vercel       │ │   │  │
│  │                                          │ │ Jira         │ │   │  │
│  │                                          │ │ Confluence   │ │   │  │
│  │                                          │ └──────────────┘ │   │  │
│  │                                          └──────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬──────────────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────────────┐
│                    SUPABASE (PostgreSQL)                               │
│  Tables: users, role_tasks, onboarding_sessions, developer_task_state │
│          conversation_logs, checklist_templates, checklist_items,      │
│          completed_verify_tasks                                       │
│  Connection: IPv4 Session Pooler (aws-0-ap-southeast-1.pooler)        │
└───────────────────────────────────────────────────────────────────────┘
```

### Agent Flow (LangGraph State Machine)

```
User Message
     │
     ▼
┌──────────┐   progress=0   ┌─────────────┐
│Supervisor│───────────────▶│ Onboarding  │
│  Router  │                │    Node     │
└────┬─────┘                └─────────────┘
     │ classify intent
     ├─── 'task'    ──▶ Task Node (get_current_task / mark_task_complete / delegate_to_hermes)
     ├─── 'github'  ──▶ GitHub Node (get_open_pull_requests / get_recent_commits / get_repository_issues)
     ├─── 'rag'     ──▶ RAG Node (search_corporate_knowledge via ChromaDB)
     └─── 'general' ──▶ General Chat Node
```

---

## ✨ Core Features

| Feature | Description |
|---|---|
| **🤖 Agentic AI Mentor** | LangGraph ReAct agent with intent classification, tool selection, and multi-step reasoning |
| **📋 Task State Machine** | Finite state machine tracking `pending → in_progress → submitted → verified → completed` per developer |
| **🔍 RAG Knowledge Base** | ChromaDB vector store with HuggingFace embeddings (`all-MiniLM-L6-v2`) over corporate docs |
| **🌐 Hermes MCP Gateway** | Live queries to Slack, Notion, Vercel, Jira, Confluence via Hermes Agent |
| **🔗 GitHub Integration** | Real-time PR, commit, and issue retrieval via PyGithub |
| **📊 Admin Analytics** | Dashboard with completion rates, average onboarding time, session history |
| **📧 Email Notifications** | Gmail SMTP alerts to HR upon onboarding completion |
| **✅ LLM-Verified Tasks** | `mark_task_complete` uses a secondary LLM evaluator to verify task submissions |
| **📝 Conversation Logging** | Full chat history persisted per session with transcript export |
| **🎯 Role-Based Onboarding** | Custom task sequences per role (Frontend, Backend, Full-Stack, DevOps, QA) |

---

## 🛠 Agent Tools & Capabilities

### 1. `get_current_task`
Fetches the developer's current assigned onboarding task from the state machine.
- **Input:** `user_id: str`
- **Source:** [`task_tools.py`](backend/app/core/task_tools.py)

### 2. `mark_task_complete`
Marks the current task as complete after LLM-based verification of the developer's submission.
- **Input:** `user_id: str`
- **Verification:** Uses `qwen3:4b` evaluator LLM to grade task completion evidence
- **Source:** [`task_tools.py`](backend/app/core/task_tools.py)

### 3. `delegate_to_hermes`
Routes external workspace queries to the Hermes Agent MCP Gateway for live data retrieval.
- **Input:** `query: str` (natural language)
- **Connected Apps:** Slack, Notion, Vercel, Jira, Confluence
- **Timeout:** `(10s connect, 180s read)`
- **Token Cap:** `HERMES_MAX_TOKENS=4096`
- **Source:** [`hermes_tool.py`](backend/app/core/hermes_tool.py)

### 4. `search_corporate_knowledge`
Performs semantic search over the ingested knowledge base using ChromaDB + HuggingFace embeddings.
- **Input:** `query: str`
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Source:** [`rag_tool.py`](backend/app/core/rag_tool.py)

### 5. `get_open_pull_requests`
Fetches the 5 most recent open PRs from the configured GitHub repository.
- **Source:** [`github_tools.py`](backend/app/core/github_tools.py)

### 6. `get_recent_commits`
Fetches the 5 most recent commits from the main branch.
- **Source:** [`github_tools.py`](backend/app/core/github_tools.py)

### 7. `get_repository_issues`
Fetches the 5 most recent open issues from the GitHub repository.
- **Source:** [`github_tools.py`](backend/app/core/github_tools.py)

---

## 🧰 Technology Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** `0.115+` | REST API framework with async support |
| **LangGraph** | ReAct agent orchestration with state machine routing |
| **LangChain** | Tool abstraction, prompt management, message types |
| **Ollama** | Local LLM inference (`qwen3:4b`) |
| **ChromaDB** | Vector store for RAG knowledge retrieval |
| **HuggingFace** | Embedding model (`all-MiniLM-L6-v2`) |
| **SQLAlchemy** | ORM for PostgreSQL database operations |
| **Alembic** | Database migrations |
| **Pydantic** | Settings management and schema validation |
| **PyGithub** | GitHub API integration |
| **Hermes Agent** | MCP gateway for external app connectors |

### Frontend
| Technology | Purpose |
|---|---|
| **React** `19.2` | UI framework |
| **Vite** `8.0` | Dev server and bundler |
| **React Router** `7.14` | Client-side routing |
| **Tailwind CSS** `4.2` | Utility-first styling |
| **Axios** | HTTP client (180s timeout) |
| **Framer Motion** | Animations and transitions |
| **Recharts** | Analytics charts and graphs |
| **Lucide React** | Icon library |
| **react-markdown** + `remark-gfm` | Markdown rendering in chat |
| **jsPDF** + `html2canvas` | PDF export for reports |

---

## 📁 Directory Structure

```
ONE/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry point + CORS
│   │   ├── api/                       # REST API route handlers
│   │   │   ├── auth.py                # JWT login/register
│   │   │   ├── chat.py                # LangGraph agent chat endpoint
│   │   │   ├── tasks.py               # Task management CRUD
│   │   │   ├── checklist.py           # Checklist items API
│   │   │   ├── onboarding.py          # Onboarding flow & FSM
│   │   │   ├── admin.py               # Admin dashboard API
│   │   │   ├── analytics.py           # Analytics & metrics
│   │   │   ├── docs.py                # Documentation search
│   │   │   └── knowledge.py           # Knowledge base endpoints
│   │   ├── core/                      # Core business logic
│   │   │   ├── config.py              # Pydantic Settings (env vars)
│   │   │   ├── database.py            # SQLAlchemy engine & sessions
│   │   │   ├── langgraph_agent.py     # LangGraph ReAct agent (543 lines)
│   │   │   ├── hermes_tool.py         # Hermes MCP gateway tool
│   │   │   ├── task_tools.py          # get_current_task, mark_task_complete
│   │   │   ├── github_tools.py        # GitHub PR/commit/issue tools
│   │   │   ├── rag_tool.py            # ChromaDB RAG search tool
│   │   │   ├── prompts.py             # System prompt templates
│   │   │   ├── graph_state.py         # LangGraph AgentState schema
│   │   │   ├── state.py               # FSM state definitions
│   │   │   ├── fsm.py                 # Finite state machine logic
│   │   │   ├── auth_deps.py           # JWT auth dependencies
│   │   │   ├── security.py            # Password hashing (bcrypt)
│   │   │   ├── seed_data.py           # Role-based task seed data
│   │   │   ├── demo_seed.py           # Demo environment seeder
│   │   │   ├── task_manager.py        # Task progression logic
│   │   │   ├── ingest_knowledge_base.py # KB ingestion script
│   │   │   └── reset_db.py            # Database reset utility
│   │   ├── models/                    # SQLAlchemy ORM models
│   │   │   ├── user.py                # User model
│   │   │   ├── tasks.py               # RoleTask model
│   │   │   ├── onboarding_session.py  # OnboardingSession model
│   │   │   ├── developer_task_state.py # DeveloperTaskState model
│   │   │   ├── conversation_log.py    # ConversationLog model
│   │   │   ├── checklist_item.py      # ChecklistItem model
│   │   │   ├── checklist_template.py  # ChecklistTemplate model
│   │   │   └── completed_verify_task.py # CompletedVerifyTask model
│   │   ├── services/                  # Business logic services
│   │   │   ├── llm_service.py         # LLM interaction service
│   │   │   ├── checklist_service.py   # Checklist operations
│   │   │   ├── analytics_service.py   # Analytics calculations
│   │   │   ├── docs_service.py        # Documentation service
│   │   │   ├── email_service.py       # Gmail SMTP sender
│   │   │   ├── email_template.py      # HTML email templates
│   │   │   └── hr_notification_service.py # HR completion alerts
│   │   ├── schemas/                   # Pydantic request/response schemas
│   │   └── rag/                       # RAG pipeline utilities
│   ├── knowledge_base/                # Corporate docs for RAG ingestion
│   ├── chroma_db/                     # ChromaDB persistent vector store
│   ├── alembic/                       # Database migration files
│   ├── scripts/                       # Utility scripts
│   ├── requirements.txt               # Python dependencies
│   ├── .env                           # Environment variables
│   └── .env.example                   # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx                   # React entry point
│   │   ├── App.jsx                    # Root component + routing
│   │   ├── App.css                    # Global styles
│   │   ├── index.css                  # Tailwind base imports
│   │   ├── pages/                     # Page-level components
│   │   │   ├── LoginPage.jsx
│   │   │   ├── DeveloperOnboardingHub.jsx
│   │   │   ├── DeveloperDashboardPage.jsx
│   │   │   ├── ChatPage.jsx
│   │   │   ├── ChecklistPage.jsx
│   │   │   ├── KnowledgeBasePage.jsx
│   │   │   ├── TaskVerification.jsx
│   │   │   ├── SessionDetailPage.jsx
│   │   │   ├── AdminDashboardPage.jsx
│   │   │   ├── AdminDevelopersPage.jsx
│   │   │   ├── AdminAnalyticsPage.jsx
│   │   │   └── AdminSettingsPage.jsx
│   │   ├── components/                # Reusable UI components
│   │   │   ├── Sidebar.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── ChatHistoryDrawer.jsx
│   │   │   ├── ChatTranscriptModal.jsx
│   │   │   ├── ChecklistItem.jsx
│   │   │   ├── ChecklistSidebar.jsx
│   │   │   ├── AdminLayout.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   ├── ProgressBar.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   └── SessionsTable.jsx
│   │   ├── api/                       # API client modules
│   │   ├── context/                   # React Context providers
│   │   ├── hooks/                     # Custom React hooks
│   │   ├── layouts/                   # Layout wrappers
│   │   ├── services/                  # Frontend service layer
│   │   └── assets/                    # Static assets
│   ├── package.json
│   └── vite.config.js
│
├── docs/                              # Project documentation
├── README.md                          # ← You are here
└── .gitignore
```

---

## 📋 Prerequisites

Ensure the following are installed **before** setup:

| Requirement | Version | Installation |
|---|---|---|
| **Python** | 3.10+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **Ollama** | Latest | [ollama.com/download](https://ollama.com/download) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |
| **Hermes Agent** _(optional)_ | Latest | [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) |

---

## 🔐 Environment Variables

Create `backend/.env` from the template `backend/.env.example`:

```env
# ─────────────────────────────────────────────────────
# LLM Provider (NVIDIA NIM — used for fallback/cloud)
# ─────────────────────────────────────────────────────
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxx
NVIDIA_MODEL_NAME=Qwen/Qwen3.5-397b-a17b

# ─────────────────────────────────────────────────────
# PostgreSQL (Supabase IPv4 Session Pooler)
# ─────────────────────────────────────────────────────
DATABASE_URL=postgresql://postgres:<PASSWORD>@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require

# ─────────────────────────────────────────────────────
# JWT Authentication
# ─────────────────────────────────────────────────────
JWT_SECRET_KEY=<your-256-bit-hex-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=480

# ─────────────────────────────────────────────────────
# Gmail SMTP (Onboarding Completion Emails)
# ─────────────────────────────────────────────────────
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# ─────────────────────────────────────────────────────
# HR Notification Recipient
# ─────────────────────────────────────────────────────
HR_EMAIL=hr-manager@company.com

# ─────────────────────────────────────────────────────
# ChromaDB (RAG Vector Store)
# ─────────────────────────────────────────────────────
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=one_knowledge_base

# ─────────────────────────────────────────────────────
# Application
# ─────────────────────────────────────────────────────
APP_ENV=development
FRONTEND_URL=http://localhost:5173

# ─────────────────────────────────────────────────────
# GitHub API Integration
# ─────────────────────────────────────────────────────
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
GITHUB_CLIENT_ID=Ov23xxxxxxxxxx
GITHUB_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_TARGET_REPO=your-org/your-repo

# ─────────────────────────────────────────────────────
# Hermes Agent (MCP Gateway — Optional)
# ─────────────────────────────────────────────────────
HERMES_API_URL=http://localhost:8642/v1/chat/completions
HERMES_API_KEY=hermes-local-key
HERMES_MAX_TOKENS=4096
```

> **⚠️ Important:** If using Supabase Free Tier, you **must** use the IPv4 Session Pooler endpoint (`aws-0-ap-southeast-1.pooler.supabase.com`) instead of the direct connection host (`db.xxx.supabase.co`), which is IPv6-only.

---

## 🔧 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/harshpatil110/O.N.E.git
cd ONE
```

### 2. Pull the Ollama Model

```bash
ollama pull qwen3:4b
```

Verify it's available:

```bash
ollama list
```

### 3. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
copy .env.example .env
# Edit .env with your actual credentials (see Environment Variables section above)
```

### 4. Database Initialization

```bash
# Run Alembic migrations (from backend/ directory)
alembic upgrade head

# Seed initial data (roles, tasks, demo users)
python -m app.core.seed_data
```

### 5. Knowledge Base Ingestion (RAG)

Place your corporate documentation files (`.txt`, `.md`, `.pdf`) in `backend/knowledge_base/`, then run:

```bash
python -m app.core.ingest_knowledge_base
```

This builds the ChromaDB vector index at `backend/chroma_db/`.

### 6. Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install
```

### 7. Hermes Agent Setup (Optional — for Slack/Notion/Vercel/Jira/Confluence)

```bash
# Install Hermes Agent globally
npm install -g @anthropic/hermes-agent

# Start the Hermes MCP gateway
hermes gateway --port 8642
```

Configure your MCP connectors (Slack, Notion, etc.) in Hermes config:
- **Windows:** `%LOCALAPPDATA%\hermes\config.yaml`
- **macOS/Linux:** `~/.hermes/config.yaml`

---

## 🚀 Running the Application

You need **4 terminal windows** running simultaneously:

### Terminal 1 — Ollama LLM Server
```bash
ollama serve
```
> Runs on `http://localhost:11434`. If Ollama is already running as a system service, skip this.

### Terminal 2 — Hermes Agent Gateway _(Optional)_
```bash
hermes gateway --port 8642
```
> Runs on `http://localhost:8642`. Only needed if you want Slack/Notion/Vercel/Jira/Confluence integration.

### Terminal 3 — FastAPI Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1   # or source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
> API available at `http://localhost:8000`
> Docs at `http://localhost:8000/docs`

### Terminal 4 — Vite React Frontend
```bash
cd frontend
npm run dev
```
> App available at `http://localhost:5173`

### Quick Health Check

```bash
# Backend health
curl http://localhost:8000/health
# Expected: {"status": "ok", "service": "O.N.E Backend"}

# Ollama health
curl http://localhost:11434/api/tags
# Expected: JSON listing available models including qwen3:4b
```

---

## 🔌 API Endpoints

All API routes are prefixed with `/api/v1/`.

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/login` | JWT login with email/password |
| `POST` | `/api/v1/auth/register` | Register new developer |
| `GET` | `/api/v1/auth/me` | Get current user profile |

### Chat (LangGraph Agent)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/chat/send` | Send message to LangGraph agent |
| `GET` | `/api/v1/chat/history/{session_id}` | Retrieve chat history |
| `GET` | `/api/v1/chat/sessions` | List all chat sessions |

### Onboarding
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/onboarding/start` | Begin onboarding flow |
| `GET` | `/api/v1/onboarding/status` | Get onboarding progress |
| `POST` | `/api/v1/onboarding/role` | Set developer role |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/tasks/current` | Get current assigned task |
| `POST` | `/api/v1/tasks/complete` | Submit task for verification |
| `GET` | `/api/v1/tasks/history` | Get completed task history |

### Checklist
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/checklist` | Get checklist items |
| `PUT` | `/api/v1/checklist/{id}` | Toggle checklist item |

### Admin
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/developers` | List all developers |
| `GET` | `/api/v1/admin/analytics` | Aggregated onboarding metrics |
| `GET` | `/api/v1/admin/sessions` | All onboarding sessions |

### Documentation
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/docs/search` | Search knowledge base (RAG) |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/analytics/overview` | Onboarding analytics overview |
| `GET` | `/api/v1/analytics/completion-rates` | Task completion statistics |

---

## 🗃 Database Schema

```mermaid
erDiagram
    users {
        uuid id PK
        string email UK
        string name
        string password_hash
        string role
        int tasks_completed
        boolean is_admin
        boolean onboarding_complete
        timestamp created_at
    }
    
    role_tasks {
        uuid id PK
        string role
        int step_number
        string title
        text description
        string verification_type
    }
    
    developer_task_state {
        uuid id PK
        uuid user_id FK
        uuid role_task_id FK
        string status
        text evidence
        timestamp started_at
        timestamp completed_at
    }
    
    onboarding_sessions {
        uuid id PK
        uuid user_id FK
        timestamp started_at
        timestamp ended_at
        string status
    }
    
    conversation_logs {
        uuid id PK
        uuid user_id FK
        uuid session_id FK
        string role
        text content
        timestamp created_at
    }
    
    checklist_templates {
        uuid id PK
        string role
        string title
        text description
        int order_index
    }
    
    checklist_items {
        uuid id PK
        uuid user_id FK
        uuid template_id FK
        boolean is_completed
        timestamp completed_at
    }
    
    completed_verify_tasks {
        uuid id PK
        uuid user_id FK
        uuid task_id FK
        text verification_result
        boolean passed
        timestamp verified_at
    }

    users ||--o{ developer_task_state : "has tasks"
    users ||--o{ onboarding_sessions : "has sessions"
    users ||--o{ conversation_logs : "has chats"
    users ||--o{ checklist_items : "has checklist"
    users ||--o{ completed_verify_tasks : "has verifications"
    role_tasks ||--o{ developer_task_state : "tracked by"
    onboarding_sessions ||--o{ conversation_logs : "contains"
    checklist_templates ||--o{ checklist_items : "instantiated as"
```

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><strong>❌ Database connection fails (IPv6 DNS resolution error)</strong></summary>

**Symptom:** `socket.gaierror: [Errno 11001] getaddrinfo failed` or `Name or service not known`

**Fix:** Switch from the Supabase direct connection to the IPv4 Session Pooler:
```env
# ❌ Direct (IPv6-only on Free Tier)
DATABASE_URL=postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres

# ✅ Session Pooler (IPv4-compatible)
DATABASE_URL=postgresql://postgres:PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
```
</details>

<details>
<summary><strong>❌ Ollama connection refused</strong></summary>

**Symptom:** `ConnectionError: HTTPConnectionPool(host='localhost', port=11434)`

**Fix:**
1. Ensure Ollama is running: `ollama serve`
2. Verify the model is pulled: `ollama list` (should show `qwen3:4b`)
3. Check port is not blocked: `netstat -an | findstr 11434`
</details>

<details>
<summary><strong>❌ Hermes Agent timeout</strong></summary>

**Symptom:** `ReadTimeout` after 180 seconds when querying Slack/Vercel

**Fix:**
- Use specific queries instead of broad ones: _"Show latest 3 Vercel deployments for project X"_ instead of _"Show all deployments"_
- Ensure `HERMES_MAX_TOKENS=4096` is set in `backend/.env`
- Check Hermes gateway is running: `curl http://localhost:8642/health`
</details>

<details>
<summary><strong>❌ CORS errors in browser console</strong></summary>

**Symptom:** `Access-Control-Allow-Origin` blocked

**Fix:** Ensure your frontend URL is in the CORS origins list in [`backend/app/main.py`](backend/app/main.py):
```python
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
]
```
</details>

<details>
<summary><strong>❌ ChromaDB / RAG returns empty results</strong></summary>

**Symptom:** `search_corporate_knowledge` returns no results

**Fix:**
1. Add `.txt` or `.md` docs to `backend/knowledge_base/`
2. Re-run ingestion: `python -m app.core.ingest_knowledge_base`
3. Verify `backend/chroma_db/` has data files
</details>

<details>
<summary><strong>❌ Frontend shows "Network Error" or blank page</strong></summary>

**Fix:**
1. Ensure backend is running on port `8000`
2. Check `frontend/src/api/config.js` points to `http://localhost:8000`
3. Try hard refresh: `Ctrl + Shift + R`
</details>

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is developed as part of an academic/enterprise initiative. Contact the repository owner for licensing details.

---

<div align="center">

**Built with ❤️ by the O.N.E. Team**

_Powered by LangGraph • Ollama • FastAPI • React • Supabase • Hermes Agent_

</div>
