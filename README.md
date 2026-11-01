<div align="center">

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
```
