#!/usr/bin/env python3
"""
generate_kb.py — Nexus AI Innovations Synthetic Knowledge Base Generator
=========================================================================
Generates ~95-100 structured Markdown files for the O.N.E. RAG pipeline.
Output: backend/knowledge_base/

Usage:
    python scripts/generate_kb.py
"""

import os
import random
import textwrap

# ─── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "knowledge_base")

# ─── Ground-truth constants ───────────────────────────────────────────────────
COMPANY = "Nexus AI Innovations"
TECH_STACK = [
    "React", "Vite", "Tailwind CSS", "Python", "FastAPI",
    "PostgreSQL (Supabase)", "Redis", "LangChain",
    "Hermes Agent (Supervisor)", "Ollama (Local LLMs)", "ChromaDB",
]
PERSONNEL = {
    "harshvardhan": {
        "name": "Harshvardhan Patil",
        "role": "Lead Systems Architect / Master Admin",
        "email": "harshvardhan@nexusai.dev",
        "github": "@harshvardhan-patil",
        "slack": "#arch-decisions",
    },
    "parth": {
        "name": "Parth Shah",
        "role": "Senior Data Engineer",
        "email": "parth@nexusai.dev",
        "github": "@parth-shah",
        "slack": "#data-eng",
    },
    "manas": {
        "name": "Manas Gupta",
        "role": "Frontend Specialist",
        "email": "manas@nexusai.dev",
        "github": "@manas-gupta",
        "slack": "#frontend",
    },
    "archit": {
        "name": "Archit Verma",
        "role": "Backend Engineer",
        "email": "archit@nexusai.dev",
        "github": "@archit-verma",
        "slack": "#backend",
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# SECTION A — CORE DICTIONARY (25-30 hardcoded, detailed files)
# ═════════════════════════════════════════════════════════════════════════════

CORE_FILES: dict[str, str] = {}

# ── 01  HR & Culture ─────────────────────────────────────────────────────────

CORE_FILES["01_hr_and_culture/code_of_ethics.md"] = textwrap.dedent(f"""\
    # {COMPANY} — Code of Ethics & Professional Conduct

    ## 1. Purpose
    This document establishes the ethical framework that every employee of
    **{COMPANY}** must uphold. It applies to full-time, part-time, and
    contract personnel across all departments.

    ## 2. Core Principles
    * **Integrity** — All business dealings must be transparent and honest.
    * **Respect** — Treat colleagues, clients, and partners with dignity.
    * **Accountability** — Own your mistakes and learn from them.
    * **Confidentiality** — Protect proprietary algorithms, client data, and
      internal communications.

    ## 3. Anti-Harassment Policy
    {COMPANY} enforces a zero-tolerance policy towards harassment of any
    kind. Report incidents to HR via `hr@nexusai.dev` or the anonymous
    Slack channel `#speak-up`.

    ## 4. Conflict of Interest
    Employees must disclose any external consulting, advisory, or
    investment activities that may conflict with {COMPANY}'s interests.
    Disclosures are submitted through the internal HR portal under
    **My Profile → Disclosures**.

    ## 5. Data Privacy Compliance
    All employees must complete the annual **Data Privacy & GDPR
    Awareness** training module within 30 days of their start date.
    Failure to comply will result in restricted system access.

    ## 6. Disciplinary Process
    | Severity | Action                          |
    |----------|---------------------------------|
    | Minor    | Verbal warning + coaching       |
    | Moderate | Written warning + PIP           |
    | Major    | Suspension pending investigation|
    | Critical | Termination + legal review      |

    ---
    *Last updated: Q2 2026 — HR Department*
""")

CORE_FILES["01_hr_and_culture/pto_leave_policy.md"] = textwrap.dedent(f"""\
    # Paid Time Off (PTO) & Leave Policy

    ## Overview
    {COMPANY} provides a flexible PTO system designed to promote work-life
    balance while maintaining project delivery commitments.

    ## Annual Allocations
    | Leave Type        | Days / Year | Carry-Over |
    |-------------------|-------------|------------|
    | Vacation          | 20          | Up to 5    |
    | Sick Leave        | 12          | None       |
    | Personal Days     | 3           | None       |
    | Bereavement       | 5           | N/A        |
    | Parental Leave    | 16 weeks    | N/A        |

    ## Request Process
    1. Submit requests via the **Nexus HR Portal** at least **5 business
       days** in advance for planned leave.
    2. For sick leave, notify your team lead via Slack before 9:00 AM IST.
    3. All requests require **manager approval** within 48 hours.

    ## Blackout Periods
    * Sprint Demo weeks (last week of each sprint).
    * Major release windows (published in `#release-calendar`).

    ## Emergency Leave
    For unforeseen emergencies, contact HR directly at `hr@nexusai.dev`.
    Retroactive PTO approval is granted on a case-by-case basis.

    ---
    *Policy Owner: HR Department — {COMPANY}*
""")

CORE_FILES["01_hr_and_culture/remote_work_policy.md"] = textwrap.dedent(f"""\
    # Remote Work & Hybrid Policy

    ## Eligibility
    All employees at **{COMPANY}** who have completed their 90-day
    probation period are eligible for hybrid remote work.

    ## Hybrid Schedule
    * **In-office days:** Tuesday and Thursday (mandatory).
    * **Remote days:** Monday, Wednesday, Friday (flexible).
    * Core hours: **10:00 AM – 4:00 PM IST** regardless of location.

    ## Remote Work Requirements
    * Minimum **50 Mbps** internet connection.
    * Dedicated workspace free from distractions.
    * Camera-on policy for all standup and sprint planning meetings.
    * VPN must be active when accessing internal resources (see
      `02_onboarding/vpn_setup.md`).

    ## Equipment Stipend
    New employees receive a one-time **₹25,000** home office setup
    stipend. Submit receipts via the Expense portal within 60 days.

    ## Communication Standards
    * Respond to Slack messages within **2 hours** during core hours.
    * Async updates must be posted in the relevant project channel by EOD.
    * Use `@here` sparingly; prefer `@channel` only for P0 incidents.

    ---
    *Policy Owner: People Operations — {COMPANY}*
""")

CORE_FILES["01_hr_and_culture/performance_reviews.md"] = textwrap.dedent(f"""\
    # Performance Review Framework

    ## Review Cadence
    {COMPANY} conducts formal performance reviews **twice per year**:
    * **Mid-Year Review:** July (formative — no rating).
    * **Annual Review:** January (summative — tied to compensation).

    ## Evaluation Criteria
    1. **Technical Output** (40%) — Code quality, system reliability, PR
       review turnaround.
    2. **Collaboration** (25%) — Cross-team contributions, mentorship,
       knowledge sharing.
    3. **Initiative** (20%) — Proactive identification and resolution of
       technical debt, process improvements.
    4. **Growth** (15%) — Completion of learning objectives, certifications,
       conference participation.

    ## Rating Scale
    | Rating     | Description                              |
    |------------|------------------------------------------|
    | Exceptional| Consistently exceeds all expectations    |
    | Strong     | Meets and often exceeds expectations     |
    | Solid      | Meets expectations reliably              |
    | Developing | Partially meets expectations; PIP issued |
    | Below      | Does not meet expectations               |

    ## Self-Assessment
    Employees must submit a self-assessment document at least **7 days**
    before their scheduled review meeting. Templates are available at
    `templates/self_assessment_2026.md`.

    ## Promotion Criteria
    Promotions require:
    * Two consecutive "Strong" or higher ratings.
    * Sponsorship from a senior engineer or architect.
    * Demonstrated impact on at least one cross-team initiative.

    ---
    *Framework Owner: Engineering Management — {COMPANY}*
""")

CORE_FILES["01_hr_and_culture/benefits_overview.md"] = textwrap.dedent(f"""\
    # Employee Benefits Overview

    ## Health & Wellness
    * Comprehensive medical, dental, and vision insurance for employees
      and dependents (covered 100% by {COMPANY}).
    * Annual wellness stipend of **₹15,000** for gym memberships, mental
      health apps, or ergonomic equipment.
    * Free access to the **Headspace** and **Calm** meditation platforms.

    ## Financial Benefits
    * Provident Fund (PF) contributions as per statutory requirements.
    * Employee Stock Option Plan (ESOP) vesting over 4 years with a
      1-year cliff.
    * Annual performance bonus pool (5-15% of base salary).

    ## Professional Development
    * **₹50,000/year** learning budget for courses, books, and
      certifications (Udemy, Coursera, O'Reilly).
    * 2 paid conference days per year (travel expenses covered).
    * Internal Tech Talk Fridays — present and earn recognition credits.

    ## Perks
    * Daily catered lunch in-office.
    * Monthly team outings budget of ₹3,000 per person.
    * Birthday day off (automatic PTO credit).

    ---
    *Benefits Administrator: People Ops — {COMPANY}*
""")

# ── 02  Onboarding ───────────────────────────────────────────────────────────

CORE_FILES["02_onboarding/day_one_checklist.md"] = textwrap.dedent(f"""\
    # Day 1 Onboarding Checklist — {COMPANY}

    Welcome to **{COMPANY}**! Complete these items on your first day.

    ## Before You Start
    - [ ] Accept your offer letter and sign the NDA via DocuSign.
    - [ ] Set up your `@nexusai.dev` Google Workspace account.
    - [ ] Download Slack and join the `#general` and `#engineering` channels.

    ## Morning (10:00 AM – 12:30 PM)
    - [ ] Attend the **Welcome Session** with HR (Google Meet link in calendar).
    - [ ] Collect your hardware (MacBook Pro M3 or equivalent).
    - [ ] Install required software:
      ```bash
      # macOS
      brew install python@3.12 node@20 docker git
      brew install --cask visual-studio-code slack
      ```
    - [ ] Clone the monorepo:
      ```bash
      git clone git@github.com:nexusai/one-platform.git
      cd one-platform
      ```

    ## Afternoon (1:30 PM – 5:00 PM)
    - [ ] Complete VPN setup (see `02_onboarding/vpn_setup.md`).
    - [ ] Generate and upload SSH keys to GitHub (see
      `02_onboarding/github_ssh_setup.md`).
    - [ ] Request Jira Cloud access from {PERSONNEL["parth"]["name"]}
      via Slack DM.
    - [ ] Set up your local development environment:
      ```bash
      cd backend && pip install -r requirements.txt
      cd ../frontend && npm install
      ```
    - [ ] Run the test suite to verify your setup:
      ```bash
      cd backend && pytest --tb=short
      cd ../frontend && npm run test
      ```

    ## End of Day
    - [ ] Post a brief introduction in `#introductions` on Slack.
    - [ ] Schedule a 1:1 with your assigned buddy for Day 2.

    ---
    *Onboarding Coordinator: HR Team — {COMPANY}*
""")

CORE_FILES["02_onboarding/vpn_setup.md"] = textwrap.dedent(f"""\
    # VPN Configuration Guide

    ## Overview
    All remote access to {COMPANY}'s internal network **requires** an
    active VPN connection. We use **WireGuard** as our VPN solution.

    ## Prerequisites
    * Your `@nexusai.dev` credentials (provided by IT on Day 1).
    * WireGuard client installed on your machine.

    ## Installation
    ```bash
    # macOS
    brew install wireguard-tools

    # Ubuntu/Debian
    sudo apt install wireguard

    # Windows
    # Download from https://www.wireguard.com/install/
    ```

    ## Configuration Steps
    1. Request your configuration file from IT via `#it-support` on Slack.
    2. Save the `.conf` file to a secure location:
       ```bash
       mkdir -p ~/.config/wireguard
       mv ~/Downloads/nexus-vpn.conf ~/.config/wireguard/
       ```
    3. Import the configuration:
       ```bash
       sudo wg-quick up ~/.config/wireguard/nexus-vpn.conf
       ```
    4. Verify the connection:
       ```bash
       curl -s https://internal.nexusai.dev/health
       # Expected: {{"status": "ok", "network": "internal"}}
       ```

    ## Troubleshooting
    | Issue                          | Solution                          |
    |--------------------------------|-----------------------------------|
    | Handshake timeout              | Check firewall rules (port 51820) |
    | DNS resolution failure         | Set DNS to `10.0.0.1`             |
    | Connection drops after 5 min   | Update WireGuard to latest        |

    ## Security Notice
    * **Never** share your VPN configuration file.
    * Report lost/compromised configs to IT immediately.
    * VPN sessions are logged for audit purposes.

    ---
    *IT Operations — {COMPANY}*
""")

CORE_FILES["02_onboarding/github_ssh_setup.md"] = textwrap.dedent(f"""\
    # GitHub SSH Key Setup

    ## Why SSH?
    {COMPANY} requires SSH-based authentication for all Git operations.
    HTTPS-based cloning is disabled on our GitHub organization.

    ## Step 1: Generate an SSH Key
    ```bash
    ssh-keygen -t ed25519 -C "your.name@nexusai.dev" -f ~/.ssh/nexusai_ed25519
    ```
    When prompted for a passphrase, choose a strong one and store it in
    your password manager.

    ## Step 2: Add to SSH Agent
    ```bash
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/nexusai_ed25519
    ```

    ## Step 3: Configure SSH for GitHub
    Add to `~/.ssh/config`:
    ```
    Host github.com
      HostName github.com
      User git
      IdentityFile ~/.ssh/nexusai_ed25519
      AddKeysToAgent yes
    ```

    ## Step 4: Upload Public Key to GitHub
    ```bash
    cat ~/.ssh/nexusai_ed25519.pub | pbcopy  # macOS
    # Then paste into GitHub → Settings → SSH Keys → New SSH Key
    ```

    ## Step 5: Verify
    ```bash
    ssh -T git@github.com
    # Expected: "Hi <username>! You've successfully authenticated..."
    ```

    ## Organization Access
    After adding your key, request org access from
    {PERSONNEL["harshvardhan"]["name"]} ({PERSONNEL["harshvardhan"]["email"]}).
    You'll receive an invitation to the `nexusai` GitHub organization.

    ---
    *DevOps — {COMPANY}*
""")

CORE_FILES["02_onboarding/jira_access_setup.md"] = textwrap.dedent(f"""\
    # Jira Cloud Access & Project Configuration

    ## Overview
    {COMPANY} uses **Jira Cloud** for project management, sprint planning,
    and issue tracking. Access is provisioned through our MCP (Model
    Context Protocol) integration.

    ## Requesting Access
    1. Send a Slack DM to {PERSONNEL["parth"]["name"]}
       ({PERSONNEL["parth"]["email"]}) with your `@nexusai.dev` email.
    2. You will receive a Jira invitation within 4 hours.
    3. Accept the invitation and set up 2FA immediately.

    ## Project Boards
    | Board Name       | Key   | Lead                             |
    |------------------|-------|----------------------------------|
    | O.N.E Platform   | ONE   | {PERSONNEL["harshvardhan"]["name"]} |
    | Data Pipeline    | DATA  | {PERSONNEL["parth"]["name"]}       |
    | Frontend UI      | FEUI  | {PERSONNEL["manas"]["name"]}       |
    | Backend Services | BSVC  | {PERSONNEL["archit"]["name"]}      |

    ## Workflow States
    ```
    Backlog → To Do → In Progress → Code Review → QA → Done
    ```

    ## MCP Integration
    The O.N.E. system reads and writes Jira issues via the **MCP Jira
    Server**. The agent can:
    * Create issues: `mcp_jira_create_issue`
    * Transition issues: `mcp_jira_transition_issue`
    * Add comments: `mcp_jira_add_comment`
    * Query sprints: `mcp_jira_get_sprint`

    ## Best Practices
    * Always link PRs to Jira tickets using the ticket key (e.g., `ONE-42`).
    * Update ticket status **before** submitting a PR for review.
    * Log time spent on each ticket for sprint velocity tracking.

    ---
    *Project Management — {COMPANY}*
""")

CORE_FILES["02_onboarding/local_dev_environment.md"] = textwrap.dedent(f"""\
    # Local Development Environment Setup

    ## System Requirements
    * **OS:** macOS 13+, Ubuntu 22.04+, or Windows 11 with WSL2.
    * **RAM:** Minimum 16 GB (32 GB recommended for Ollama models).
    * **Storage:** 50 GB free SSD space.

    ## Backend Setup (Python / FastAPI)
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
    pip install -r requirements.txt

    # Copy environment template
    cp .env.example .env
    # Edit .env with your Supabase credentials, JWT secrets, etc.

    # Run the development server
    uvicorn app.main:app --reload --port 8000
    ```

    ## Frontend Setup (React / Vite)
    ```bash
    cd frontend
    npm install

    # Start Vite dev server
    npm run dev  # Default: http://localhost:5173
    ```

    ## Database (Supabase / PostgreSQL)
    The team uses a shared Supabase instance. Connection string format:
    ```
    DATABASE_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
    ```
    Contact {PERSONNEL["harshvardhan"]["name"]} for credentials.

    ## ChromaDB (Local Vector Store)
    ```bash
    # ChromaDB is embedded; it starts automatically with the backend.
    # Data is persisted to ./chroma_db/
    CHROMA_PERSIST_DIRECTORY=./chroma_db
    CHROMA_COLLECTION_NAME=one_knowledge_base
    ```

    ## Ollama (Local LLM)
    ```bash
    # Install Ollama
    curl -fsSL https://ollama.com/install.sh | sh

    # Pull the default model
    ollama pull qwen2.5:7b
    ```

    ## Verifying Everything Works
    ```bash
    # Backend health check
    curl http://localhost:8000/health
    # Expected: {{"status": "ok", "service": "O.N.E Backend"}}

    # Frontend
    # Open http://localhost:5173 in your browser
    ```

    ---
    *Engineering Onboarding — {COMPANY}*
""")

# ── 03  Architecture ─────────────────────────────────────────────────────────

CORE_FILES["03_architecture/system_overview.md"] = textwrap.dedent(f"""\
    # {COMPANY} — O.N.E. Platform Architecture Overview

    ## System Purpose
    The **O.N.E. (Onboarding Navigation Environment)** platform is an
    AI-powered multi-agent system that guides new employees through their
    complete onboarding journey at {COMPANY}.

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
    *Architecture maintained by {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["03_architecture/fastapi_backend_structure.md"] = textwrap.dedent(f"""\
    # FastAPI Backend Directory Structure

    ## Layout
    ```
    backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py              # FastAPI app init, middleware, router mounts
    │   ├── api/
    │   │   ├── auth.py          # POST /auth/login, /auth/register
    │   │   ├── chat.py          # POST /chat/{{session_id}}/message
    │   │   ├── onboarding.py    # GET/POST onboarding sessions
    │   │   ├── checklist.py     # CRUD for checklist items
    │   │   ├── admin.py         # Admin-only endpoints
    │   │   ├── analytics.py     # Dashboard metrics
    │   │   └── docs.py          # Knowledge base document access
    │   ├── agents/
    │   │   ├── orchestrator.py  # AgentOrchestrator (Hermes dispatcher)
    │   │   ├── rag_agent.py     # RAG retrieval sub-agent
    │   │   └── tools/           # MCP tool definitions
    │   ├── core/
    │   │   ├── config.py        # Pydantic Settings (env vars)
    │   │   ├── database.py      # SQLAlchemy engine + SessionLocal
    │   │   ├── security.py      # bcrypt hashing, JWT creation
    │   │   └── auth_deps.py     # FastAPI dependency injection for auth
    │   ├── models/
    │   │   ├── user.py          # User ORM model
    │   │   └── onboarding_session.py
    │   └── schemas/
    │       ├── auth.py          # LoginRequest, TokenResponse
    │       ├── chat.py          # ChatMessageRequest/Response
    │       └── admin.py         # Admin-specific schemas
    ├── scripts/
    │   ├── generate_kb.py       # This script
    │   └── seed_admin.py        # Admin account seeder
    ├── knowledge_base/          # Generated markdown files (RAG source)
    ├── chroma_db/               # ChromaDB persistence directory
    ├── requirements.txt
    └── .env
    ```

    ## Key Design Decisions
    * **Dependency Injection:** All auth checks use FastAPI `Depends()`.
    * **ORM:** SQLAlchemy 2.0 with declarative models.
    * **Migrations:** Alembic for schema versioning.
    * **CORS:** Configured in `main.py` to allow frontend origins.

    ---
    *Backend Lead: {PERSONNEL["archit"]["name"]}*
""")

CORE_FILES["03_architecture/react_frontend_structure.md"] = textwrap.dedent(f"""\
    # React Frontend Architecture

    ## Tech Stack
    * **Framework:** React 18 with functional components and hooks.
    * **Bundler:** Vite 5 (HMR, ESBuild-powered).
    * **Styling:** Tailwind CSS 3.4 with custom design tokens.
    * **Routing:** React Router v6.
    * **State:** React Context API (AuthContext, ChecklistContext).
    * **HTTP:** Axios for API communication.
    * **Animations:** Framer Motion.

    ## Directory Structure
    ```
    frontend/
    ├── src/
    │   ├── api/
    │   │   ├── auth.js          # login(), register()
    │   │   ├── chat.js          # sendMessage(), getChatHistory()
    │   │   └── admin.js         # getDevelopers(), getAnalytics()
    │   ├── components/
    │   │   ├── ChatUI.jsx       # Main chat interface
    │   │   ├── MessageBubble.jsx
    │   │   ├── ChatHistoryDrawer.jsx
    │   │   └── Sidebar.jsx
    │   ├── context/
    │   │   ├── AuthContext.jsx   # AuthProvider (token + role)
    │   │   └── ChecklistContext.jsx
    │   ├── hooks/
    │   │   ├── useAuth.js
    │   │   └── useChat.js       # Chat message lifecycle
    │   ├── pages/
    │   │   ├── LoginPage.jsx
    │   │   ├── DashboardPage.jsx
    │   │   └── AdminDevelopersPage.jsx
    │   ├── index.css            # Global styles + scrollbar overrides
    │   └── main.jsx             # App entry point
    ├── index.html
    ├── vite.config.js
    ├── tailwind.config.js
    └── package.json
    ```

    ## Key Patterns
    * **Token Storage:** `sessionStorage` (not localStorage) for JWT.
    * **Role-Based Routing:** Admin users redirect to `/admin`;
      employees go to `/dashboard`.
    * **Optimistic Updates:** Chat messages appear immediately before
      server confirmation.

    ---
    *Frontend Lead: {PERSONNEL["manas"]["name"]}*
""")

CORE_FILES["03_architecture/hermes_agent_router.md"] = textwrap.dedent(f"""\
    # Hermes Agent — Supervisor Router Architecture

    ## Overview
    The **Hermes Agent** acts as the central supervisor in {COMPANY}'s
    multi-agent architecture. It receives user intents from the
    `AgentOrchestrator` and routes them to the appropriate sub-agent.

    ## Router Diagram
    ```
    User Message
        │
        ▼
    ┌───────────────────────┐
    │   AgentOrchestrator   │
    │   (app/agents/        │
    │    orchestrator.py)   │
    └──────────┬────────────┘
               │
               ▼
    ┌───────────────────────┐
    │   Hermes Supervisor   │
    │   (LangChain Agent)   │
    │                       │
    │   Tools Available:    │
    │   ├─ rag_search       │
    │   ├─ jira_create      │
    │   ├─ jira_query       │
    │   ├─ github_pr_list   │
    │   ├─ github_repo_info │
    │   ├─ send_email       │
    │   └─ update_checklist │
    └──────────┬────────────┘
               │
        ┌──────┼──────┐
        ▼      ▼      ▼
    ┌──────┐┌──────┐┌──────┐
    │ RAG  ││ Jira ││GitHub│
    │Agent ││ MCP  ││ MCP  │
    └──────┘└──────┘└──────┘
    ```

    ## Routing Logic
    The Hermes supervisor uses the LLM's function-calling capability to
    decide which tool to invoke. The decision is based on:
    1. **Intent Classification:** The LLM classifies the user message.
    2. **Tool Selection:** Based on the classified intent, the LLM
       selects the appropriate tool and generates arguments.
    3. **Execution:** The selected tool is executed and the result is
       returned to the LLM for response generation.

    ## Sub-Agent Details
    | Agent       | Responsibility                              |
    |-------------|---------------------------------------------|
    | RAG Agent   | Search the knowledge base via ChromaDB       |
    | Jira MCP    | Create/query/transition Jira issues          |
    | GitHub MCP  | List PRs, check repo status, read files      |
    | Email Tool  | Send completion reports to HR                |
    | Checklist   | Update onboarding progress in the database   |

    ---
    *Architect: {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["03_architecture/chromadb_chunking_rules.md"] = textwrap.dedent(f"""\
    # ChromaDB Chunking & Embedding Rules

    ## Overview
    The RAG pipeline in {COMPANY}'s O.N.E. platform uses **ChromaDB** as
    the vector store for document embeddings. This document specifies the
    chunking strategy.

    ## Chunking Strategy
    * **Method:** Recursive Character Text Splitter (LangChain).
    * **Chunk Size:** 1000 characters.
    * **Chunk Overlap:** 200 characters.
    * **Separators:** `["\\n## ", "\\n### ", "\\n\\n", "\\n", " "]`

    ## Why These Settings?
    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\\n## ", "\\n### ", "\\n\\n", "\\n", " "],
    )
    ```
    * **1000 chars** keeps chunks within the embedding model's sweet spot.
    * **200 char overlap** prevents information loss at chunk boundaries.
    * **Markdown-aware separators** ensure headers stay with their content.

    ## Embedding Model
    * **Model:** `nomic-embed-text` via Ollama (768-dim vectors).
    * **Batch Size:** 64 documents per batch.
    * **Collection:** `one_knowledge_base`

    ## Metadata Attached to Each Chunk
    ```json
    {{
        "source": "03_architecture/system_overview.md",
        "chunk_index": 0,
        "total_chunks": 5,
        "category": "architecture",
        "created_at": "2026-08-01T00:00:00Z"
    }}
    ```

    ## Re-indexing Procedure
    ```bash
    cd backend
    python scripts/ingest_kb.py --force-rebuild
    ```
    This drops the existing collection and re-indexes all files from
    `knowledge_base/`.

    ---
    *Data Engineering: {PERSONNEL["parth"]["name"]}*
""")

# ── 04  Coding Standards ─────────────────────────────────────────────────────

CORE_FILES["04_coding_standards/python_style_guide.md"] = textwrap.dedent(f"""\
    # Python Coding Standards — {COMPANY}

    ## General Rules
    * Follow **PEP 8** strictly. Use `ruff` as the primary linter.
    * Maximum line length: **88 characters** (Black formatter default).
    * Use **type hints** for all function signatures.

    ## Formatting
    ```bash
    # Auto-format before committing
    ruff format .
    ruff check --fix .
    ```

    ## Naming Conventions
    | Element       | Convention          | Example                    |
    |---------------|---------------------|----------------------------|
    | Variables     | snake_case          | `user_count`               |
    | Functions     | snake_case          | `get_active_users()`       |
    | Classes       | PascalCase          | `OnboardingSession`        |
    | Constants     | UPPER_SNAKE_CASE    | `MAX_RETRY_COUNT`          |
    | Modules       | snake_case          | `auth_deps.py`             |

    ## Docstrings
    Use Google-style docstrings:
    ```python
    def create_user(email: str, role: str) -> User:
        \"\"\"Create a new user in the database.

        Args:
            email: The user's email address.
            role: The user's role (e.g., 'admin', 'engineer').

        Returns:
            The newly created User ORM instance.

        Raises:
            ValueError: If the email already exists.
        \"\"\"
    ```

    ## Import Order
    1. Standard library
    2. Third-party packages
    3. Local application imports

    Enforced by `ruff` rule `I` (isort-compatible).

    ## Error Handling
    * Always use specific exception types, never bare `except:`.
    * Log exceptions with `logger.error(msg, exc_info=True)`.
    * Use FastAPI's `HTTPException` for API error responses.

    ---
    *Standards maintained by {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["04_coding_standards/react_best_practices.md"] = textwrap.dedent(f"""\
    # React & Frontend Best Practices — {COMPANY}

    ## Component Design
    * Use **functional components** exclusively (no class components).
    * Keep components under **150 lines**. Extract sub-components early.
    * Use `React.memo()` for expensive renders.

    ## Hooks Guidelines
    * Custom hooks must be prefixed with `use` (e.g., `useChat`).
    * Never call hooks conditionally or inside loops.
    * Use `useCallback` for event handlers passed as props.
    * Use `useMemo` for expensive computed values.

    ## State Management
    * Local state → `useState`
    * Cross-component state → React Context API
    * Server state → Custom hooks with Axios (no Redux needed for
      this project scale).

    ## Styling
    * Use **Tailwind CSS** utility classes directly in JSX.
    * Custom styles go in `index.css` using `@layer components`.
    * Avoid inline `style={{{{}}}}` except for dynamic values.

    ## File Naming
    | Type          | Convention            | Example              |
    |---------------|-----------------------|----------------------|
    | Components    | PascalCase.jsx        | `MessageBubble.jsx`  |
    | Hooks         | camelCase.js          | `useChat.js`         |
    | API modules   | camelCase.js          | `auth.js`            |
    | Pages         | PascalCase.jsx        | `LoginPage.jsx`      |

    ## Performance
    * Lazy-load routes with `React.lazy()` + `Suspense`.
    * Use the `key` prop correctly in `.map()` — never use array index
      as key for dynamic lists.
    * Debounce search inputs with 300ms delay.

    ---
    *Frontend Standards: {PERSONNEL["manas"]["name"]}*
""")

CORE_FILES["04_coding_standards/git_branching_strategy.md"] = textwrap.dedent(f"""\
    # Git Branching Strategy — {COMPANY}

    ## Branch Types
    | Branch        | Pattern              | Purpose                       |
    |---------------|----------------------|-------------------------------|
    | Main          | `main`               | Production-ready code         |
    | Development   | `dev`                | Integration branch            |
    | Feature       | `feature/ONE-<id>`   | New feature work              |
    | Bugfix        | `bugfix/ONE-<id>`    | Bug fixes                     |
    | Hotfix        | `hotfix/ONE-<id>`    | Critical production fixes     |
    | Release       | `release/v<semver>`  | Release preparation           |

    ## Workflow
    1. Branch off `dev` for features: `git checkout -b feature/ONE-42`.
    2. Make atomic commits with conventional messages:
       ```
       feat(chat): add streaming response support
       fix(auth): handle expired JWT gracefully
       docs(kb): update VPN setup instructions
       ```
    3. Push and open a Pull Request targeting `dev`.
    4. Request review from at least **1 peer** and **1 senior**.
    5. After approval, **squash merge** into `dev`.
    6. `dev` is merged into `main` via release branches only.

    ## PR Checklist
    - [ ] Linked to a Jira ticket (e.g., `ONE-42`).
    - [ ] Tests pass locally (`pytest` / `npm run test`).
    - [ ] No linting warnings (`ruff check .` / `eslint`).
    - [ ] Updated relevant documentation if needed.
    - [ ] Screenshots attached for UI changes.

    ## Protected Branches
    * `main` — Requires 2 approvals + passing CI.
    * `dev` — Requires 1 approval + passing CI.

    ---
    *DevOps: {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["04_coding_standards/alembic_migrations.md"] = textwrap.dedent(f"""\
    # Alembic Database Migration Guide

    ## Overview
    {COMPANY} uses **Alembic** for managing PostgreSQL schema migrations
    against our Supabase database.

    ## Setup
    ```bash
    cd backend
    alembic init alembic  # Only needed once
    ```

    ## Creating a Migration
    ```bash
    # Auto-generate from model changes
    alembic revision --autogenerate -m "add_progress_percentage_to_sessions"

    # Or create an empty migration for manual edits
    alembic revision -m "seed_initial_roles"
    ```

    ## Running Migrations
    ```bash
    # Apply all pending migrations
    alembic upgrade head

    # Rollback one step
    alembic downgrade -1

    # View current revision
    alembic current

    # View migration history
    alembic history --verbose
    ```

    ## Best Practices
    * **One migration per PR.** Never bundle unrelated schema changes.
    * Always test migrations on a local database before running against
      the Supabase production instance.
    * Include both `upgrade()` and `downgrade()` functions.
    * Use `op.execute()` for data migrations, not ORM models.

    ## Environment Configuration
    Set `sqlalchemy.url` in `alembic.ini`:
    ```ini
    sqlalchemy.url = postgresql://postgres:<pass>@db.<ref>.supabase.co:5432/postgres
    ```
    Or override via environment variable:
    ```python
    # env.py
    config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
    ```

    ---
    *Database Admin: {PERSONNEL["parth"]["name"]}*
""")

CORE_FILES["04_coding_standards/api_design_conventions.md"] = textwrap.dedent(f"""\
    # REST API Design Conventions — {COMPANY}

    ## URL Structure
    All endpoints follow the pattern:
    ```
    /api/v1/<resource>/<action>
    ```

    ## HTTP Methods
    | Method | Usage                          | Example                        |
    |--------|--------------------------------|--------------------------------|
    | GET    | Retrieve resource(s)           | `GET /api/v1/users`            |
    | POST   | Create a resource              | `POST /api/v1/auth/login`      |
    | PUT    | Full update of a resource      | `PUT /api/v1/users/{{id}}`       |
    | PATCH  | Partial update                 | `PATCH /api/v1/sessions/{{id}}`  |
    | DELETE | Remove a resource              | `DELETE /api/v1/users/{{id}}`    |

    ## Response Format
    All responses use a consistent JSON envelope:
    ```json
    {{
        "data": {{ ... }},
        "meta": {{
            "request_id": "uuid-v4",
            "timestamp": "ISO-8601"
        }}
    }}
    ```

    ## Error Responses
    ```json
    {{
        "detail": "Invalid email or password",
        "status_code": 401
    }}
    ```

    ## Authentication
    * All protected endpoints require a Bearer JWT token in the
      `Authorization` header.
    * Admin endpoints require `role == "admin"` in the JWT claims.

    ## Pagination
    Use query parameters for paginated endpoints:
    ```
    GET /api/v1/admin/developers?page=1&limit=20
    ```

    ## Rate Limiting
    * Public endpoints: 60 requests/minute per IP.
    * Authenticated endpoints: 200 requests/minute per user.
    * Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

    ---
    *API Standards: {PERSONNEL["archit"]["name"]}*
""")

# ── 05  DevOps ────────────────────────────────────────────────────────────────

CORE_FILES["05_devops/docker_compose_setup.md"] = textwrap.dedent(f"""\
    # Docker Compose — Local Development Stack

    ## Overview
    The following `docker-compose.yml` spins up the entire {COMPANY}
    development stack locally.

    ## docker-compose.yml
    ```yaml
    version: "3.9"

    services:
      backend:
        build: ./backend
        ports:
          - "8000:8000"
        env_file:
          - ./backend/.env
        volumes:
          - ./backend:/app
        depends_on:
          - redis
        command: uvicorn app.main:app --host 0.0.0.0 --reload

      frontend:
        build: ./frontend
        ports:
          - "5173:5173"
        volumes:
          - ./frontend:/app
          - /app/node_modules
        command: npm run dev -- --host

      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
        volumes:
          - redis_data:/data

      chromadb:
        image: chromadb/chroma:latest
        ports:
          - "8001:8000"
        volumes:
          - chroma_data:/chroma/chroma

    volumes:
      redis_data:
      chroma_data:
    ```

    ## Usage
    ```bash
    # Start all services
    docker compose up -d

    # View logs
    docker compose logs -f backend

    # Rebuild after dependency changes
    docker compose build --no-cache backend

    # Tear down
    docker compose down -v
    ```

    ---
    *DevOps: {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["05_devops/ci_cd_pipeline.md"] = textwrap.dedent(f"""\
    # CI/CD Pipeline Configuration

    ## Overview
    {COMPANY} uses **GitHub Actions** for continuous integration and
    deployment.

    ## Pipeline Stages
    ```
    Push to PR → Lint → Test → Build → Deploy (staging) → Manual approval → Deploy (prod)
    ```

    ## GitHub Actions Workflow
    ```yaml
    name: O.N.E CI/CD

    on:
      push:
        branches: [dev, main]
      pull_request:
        branches: [dev]

    jobs:
      lint-and-test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: "3.12"
          - name: Install dependencies
            run: |
              cd backend
              pip install -r requirements.txt
              pip install ruff pytest
          - name: Lint
            run: ruff check backend/
          - name: Test
            run: |
              cd backend
              pytest --tb=short -q
            env:
              DATABASE_URL: ${{{{ secrets.TEST_DATABASE_URL }}}}
              JWT_SECRET_KEY: test-secret-key

      frontend-build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-node@v4
            with:
              node-version: "20"
          - run: cd frontend && npm ci && npm run build
    ```

    ## Secrets Management
    All secrets are stored in **GitHub Repository Settings → Secrets**:
    * `TEST_DATABASE_URL`
    * `PROD_DATABASE_URL`
    * `JWT_SECRET_KEY`
    * `NVIDIA_API_KEY`

    ---
    *CI/CD Lead: {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["05_devops/environment_variables.md"] = textwrap.dedent(f"""\
    # Environment Variables Reference

    ## Backend `.env` Template
    ```env
    # ─── LLM Provider ───
    NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxx
    NVIDIA_MODEL_NAME=Qwen/Qwen3.5-397b-a17b

    # ─── Database ───
    DATABASE_URL=postgresql://postgres:<password>@db.<ref>.supabase.co:5432/postgres

    # ─── JWT Auth ───
    JWT_SECRET_KEY=<64-char-hex-string>
    JWT_ALGORITHM=HS256
    JWT_EXPIRY_MINUTES=480

    # ─── Email (SMTP) ───
    GMAIL_ADDRESS=notifications@nexusai.dev
    GMAIL_APP_PASSWORD=<app-password>

    # ─── HR Configuration ───
    HR_EMAIL=hr@nexusai.dev

    # ─── ChromaDB ───
    CHROMA_PERSIST_DIRECTORY=./chroma_db
    CHROMA_COLLECTION_NAME=one_knowledge_base

    # ─── App Config ───
    APP_ENV=development
    FRONTEND_URL=http://localhost:5173
    ```

    ## Frontend `.env` Template
    ```env
    VITE_API_URL=http://localhost:8000
    ```

    ## Security Rules
    * **Never** commit `.env` files to Git. Verify `.gitignore` includes
      `.env` and `.env.*`.
    * Rotate `JWT_SECRET_KEY` quarterly.
    * Use **GitHub Secrets** for CI/CD environment variables.
    * Use separate Supabase projects for `development`, `staging`, and
      `production`.

    ---
    *Security: {PERSONNEL["harshvardhan"]["name"]}*
""")

CORE_FILES["05_devops/monitoring_and_logging.md"] = textwrap.dedent(f"""\
    # Monitoring & Logging Standards

    ## Logging Framework
    All backend services use Python's `logging` module configured via
    `app/core/config.py`:

    ```python
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    ```

    ## Log Levels
    | Level    | Usage                                         |
    |----------|-----------------------------------------------|
    | DEBUG    | Detailed diagnostic (local dev only)          |
    | INFO     | Normal operations (requests, completions)     |
    | WARNING  | Unexpected but non-critical events             |
    | ERROR    | Failures requiring attention                  |
    | CRITICAL | System-level failures (DB down, OOM)          |

    ## Structured Logging for Agents
    Agent interactions log structured JSON:
    ```python
    logger.info("Agent response", extra={{
        "session_id": session.id,
        "tool_called": "rag_search",
        "query": user_message[:100],
        "response_length": len(response),
        "latency_ms": elapsed_ms,
    }})
    ```

    ## Monitoring Endpoints
    * `GET /health` — Returns `{{"status": "ok"}}` with 200.
    * `GET /health/deep` — Checks DB, Redis, and ChromaDB connectivity.

    ---
    *Observability: {PERSONNEL["archit"]["name"]}*
""")

# ── 06  Team Directory ────────────────────────────────────────────────────────

CORE_FILES["06_team_directory/harshvardhan_patil.md"] = textwrap.dedent(f"""\
    # Team Profile: {PERSONNEL["harshvardhan"]["name"]}

    ## Role
    **{PERSONNEL["harshvardhan"]["role"]}**

    ## Contact
    | Channel   | Handle                                    |
    |-----------|-------------------------------------------|
    | Email     | {PERSONNEL["harshvardhan"]["email"]}       |
    | GitHub    | {PERSONNEL["harshvardhan"]["github"]}      |
    | Slack     | {PERSONNEL["harshvardhan"]["slack"]}       |

    ## Responsibilities
    * Overall system architecture and technical direction for the O.N.E.
      platform.
    * Master Admin access to all production systems (Supabase, GitHub
      org, Jira Cloud, Ollama cluster).
    * Code review authority for all backend and infrastructure PRs.
    * Sprint planning and technical backlog grooming.
    * Research paper coordination and experiment design.

    ## Expertise
    * Multi-agent AI systems (LangChain, Hermes Supervisor pattern).
    * FastAPI microservice design.
    * PostgreSQL performance tuning.
    * DevOps and CI/CD pipeline architecture.

    ## Office Hours
    * **Tuesday & Thursday:** 2:00 PM – 4:00 PM IST (in-person).
    * **By appointment:** DM on Slack for async scheduling.

    ---
    *{COMPANY} — Engineering Team*
""")

CORE_FILES["06_team_directory/parth_shah.md"] = textwrap.dedent(f"""\
    # Team Profile: {PERSONNEL["parth"]["name"]}

    ## Role
    **{PERSONNEL["parth"]["role"]}**

    ## Contact
    | Channel   | Handle                              |
    |-----------|-------------------------------------|
    | Email     | {PERSONNEL["parth"]["email"]}        |
    | GitHub    | {PERSONNEL["parth"]["github"]}       |
    | Slack     | {PERSONNEL["parth"]["slack"]}        |

    ## Responsibilities
    * Design and maintain the RAG data pipeline (ingestion, chunking,
      embedding, and retrieval via ChromaDB).
    * Manage the Supabase PostgreSQL database schema, migrations, and
      backups.
    * Jira Cloud administration and MCP tool configuration.
    * Data quality monitoring and vector store optimization.

    ## Expertise
    * Data engineering (ETL, batch/stream processing).
    * PostgreSQL and Supabase administration.
    * ChromaDB vector store operations.
    * Alembic migrations and schema design.

    ## Office Hours
    * **Monday & Wednesday:** 3:00 PM – 5:00 PM IST.

    ---
    *{COMPANY} — Engineering Team*
""")

CORE_FILES["06_team_directory/manas_gupta.md"] = textwrap.dedent(f"""\
    # Team Profile: {PERSONNEL["manas"]["name"]}

    ## Role
    **{PERSONNEL["manas"]["role"]}**

    ## Contact
    | Channel   | Handle                               |
    |-----------|--------------------------------------|
    | Email     | {PERSONNEL["manas"]["email"]}         |
    | GitHub    | {PERSONNEL["manas"]["github"]}        |
    | Slack     | {PERSONNEL["manas"]["slack"]}         |

    ## Responsibilities
    * Develop and maintain the React/Vite/Tailwind CSS frontend for the
      O.N.E. platform.
    * Implement the chat interface, admin dashboard, and onboarding UI
      flows.
    * Ensure responsive design, accessibility (WCAG 2.1 AA), and
      performance optimization.
    * Collaborate with backend engineers on API contract design.

    ## Expertise
    * React 18 (hooks, context, lazy loading).
    * Tailwind CSS and design system implementation.
    * Framer Motion animations.
    * Vite configuration and optimization.

    ## Office Hours
    * **Tuesday & Friday:** 11:00 AM – 1:00 PM IST.

    ---
    *{COMPANY} — Engineering Team*
""")

CORE_FILES["06_team_directory/archit_verma.md"] = textwrap.dedent(f"""\
    # Team Profile: {PERSONNEL["archit"]["name"]}

    ## Role
    **{PERSONNEL["archit"]["role"]}**

    ## Contact
    | Channel   | Handle                                |
    |-----------|---------------------------------------|
    | Email     | {PERSONNEL["archit"]["email"]}         |
    | GitHub    | {PERSONNEL["archit"]["github"]}        |
    | Slack     | {PERSONNEL["archit"]["slack"]}         |

    ## Responsibilities
    * Develop and maintain FastAPI backend services (auth, chat,
      onboarding, admin, analytics endpoints).
    * Implement JWT-based authentication and role-based access control.
    * Integrate external services (Jira MCP, GitHub MCP, email SMTP).
    * Write and maintain backend unit and integration tests.

    ## Expertise
    * FastAPI and Python async programming.
    * SQLAlchemy ORM and raw SQL optimization.
    * JWT/OAuth2 security patterns.
    * Redis caching strategies.

    ## Office Hours
    * **Wednesday & Thursday:** 10:00 AM – 12:00 PM IST.

    ---
    *{COMPANY} — Engineering Team*
""")

CORE_FILES["06_team_directory/team_overview.md"] = textwrap.dedent(f"""\
    # {COMPANY} — Engineering Team Overview

    ## Mission
    Build the **O.N.E. (Onboarding Navigation Environment)** — an
    AI-powered multi-agent platform that transforms how new employees
    are onboarded at enterprise organizations.

    ## Team Composition
    | Name                      | Role                                  |
    |---------------------------|---------------------------------------|
    | {PERSONNEL["harshvardhan"]["name"]} | {PERSONNEL["harshvardhan"]["role"]} |
    | {PERSONNEL["parth"]["name"]}        | {PERSONNEL["parth"]["role"]}        |
    | {PERSONNEL["manas"]["name"]}        | {PERSONNEL["manas"]["role"]}        |
    | {PERSONNEL["archit"]["name"]}       | {PERSONNEL["archit"]["role"]}       |

    ## Communication Channels
    * **Daily Standup:** 10:00 AM IST (Google Meet, auto-scheduled).
    * **Sprint Planning:** Every other Monday, 11:00 AM IST.
    * **Retrospective:** Last Friday of each sprint, 3:00 PM IST.
    * **Emergency Channel:** `#incident-response` on Slack.

    ## Tech Stack Summary
    {chr(10).join(f"* {t}" for t in TECH_STACK)}

    ---
    *{COMPANY} — Building the Future of Employee Onboarding*
""")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION B — PROCEDURAL GENERATORS (60-70 additional files)
# ═════════════════════════════════════════════════════════════════════════════

# ── B.1  Mock FastAPI Endpoint Specs (30 files) ──────────────────────────────

API_ENDPOINTS = [
    ("GET",    "/api/v1/users",                    "List all users",                 "user",       "Returns paginated list of users with roles and creation dates."),
    ("GET",    "/api/v1/users/{user_id}",          "Get user by ID",                 "user",       "Returns a single user record including onboarding progress."),
    ("POST",   "/api/v1/users",                    "Create a new user",              "user",       "Creates a user with email, name, role, and hashed password."),
    ("PUT",    "/api/v1/users/{user_id}",          "Update user profile",            "user",       "Updates user name, role, or email. Admin-only endpoint."),
    ("DELETE", "/api/v1/users/{user_id}",          "Delete a user",                  "user",       "Soft-deletes a user record. Requires admin role."),
    ("POST",   "/api/v1/auth/login",               "Authenticate user",              "auth",       "Accepts email+password, returns JWT with sub and role claims."),
    ("POST",   "/api/v1/auth/register",            "Register new employee",          "auth",       "Creates employee account and initializes onboarding session."),
    ("POST",   "/api/v1/auth/refresh",             "Refresh JWT token",              "auth",       "Accepts a valid JWT and returns a new token with extended expiry."),
    ("POST",   "/api/v1/auth/logout",              "Invalidate session",             "auth",       "Adds current JWT to server-side denylist in Redis."),
    ("GET",    "/api/v1/onboarding/sessions",      "List onboarding sessions",       "onboarding", "Returns all sessions for the authenticated user."),
    ("POST",   "/api/v1/onboarding/sessions",      "Create onboarding session",      "onboarding", "Initializes a new onboarding session for a user."),
    ("GET",    "/api/v1/onboarding/sessions/{id}", "Get session details",            "onboarding", "Returns session metadata, progress, and checklist status."),
    ("PATCH",  "/api/v1/onboarding/sessions/{id}", "Update session progress",        "onboarding", "Updates progress_percentage and completed steps."),
    ("GET",    "/api/v1/checklist/{session_id}",   "Get checklist items",            "checklist",  "Returns all checklist items for an onboarding session."),
    ("POST",   "/api/v1/checklist/{session_id}",   "Add checklist item",             "checklist",  "Adds a new task to the session checklist."),
    ("PATCH",  "/api/v1/checklist/items/{item_id}","Toggle checklist item",          "checklist",  "Marks a checklist item as completed or incomplete."),
    ("POST",   "/api/v1/chat/{session_id}/message","Send chat message",              "chat",       "Sends user message to Hermes Agent, returns AI response."),
    ("GET",    "/api/v1/chat/{session_id}/history", "Get chat history",              "chat",       "Returns paginated chat messages for a session."),
    ("DELETE", "/api/v1/chat/{session_id}",        "Clear chat history",             "chat",       "Deletes all messages in a chat session. Admin-only."),
    ("GET",    "/api/v1/admin/developers",         "List all developers",            "admin",      "Admin endpoint returning all developer accounts with progress."),
    ("GET",    "/api/v1/admin/developers/{id}/chats","Get developer chat history",   "admin",      "Admin endpoint to view a specific developer's chat transcripts."),
    ("GET",    "/api/v1/admin/analytics",          "Get analytics dashboard data",   "admin",      "Returns onboarding metrics, completion rates, and trends."),
    ("GET",    "/api/v1/admin/analytics/timeline", "Get onboarding timeline",        "admin",      "Returns time-series data for onboarding volume charts."),
    ("GET",    "/api/v1/docs/search",              "Search knowledge base",          "docs",       "Performs RAG search against ChromaDB. Returns top-k results."),
    ("GET",    "/api/v1/docs/categories",          "List document categories",       "docs",       "Returns available KB categories and document counts."),
    ("GET",    "/api/v1/docs/{doc_id}",            "Get document content",           "docs",       "Returns full markdown content of a knowledge base document."),
    ("POST",   "/api/v1/docs/ingest",              "Ingest new document",            "docs",       "Uploads and indexes a new markdown document into ChromaDB."),
    ("GET",    "/api/v1/health",                   "Health check",                   "system",     "Returns service status. No auth required."),
    ("GET",    "/api/v1/health/deep",              "Deep health check",              "system",     "Checks DB, Redis, ChromaDB connectivity. Admin-only."),
    ("GET",    "/api/v1/system/config",            "Get system configuration",       "system",     "Returns non-sensitive system configuration. Admin-only."),
]

HTTP_STATUS_CODES = {
    "GET": ("200 OK", "404 Not Found"),
    "POST": ("201 Created", "400 Bad Request"),
    "PUT": ("200 OK", "404 Not Found"),
    "PATCH": ("200 OK", "404 Not Found"),
    "DELETE": ("204 No Content", "404 Not Found"),
}

def generate_api_spec(index: int, method: str, path: str, summary: str,
                      category: str, description: str) -> str:
    """Generate a realistic API specification markdown file."""
    success, error = HTTP_STATUS_CODES.get(method, ("200 OK", "400 Bad Request"))
    auth_required = category not in ("system",) or "deep" in path or "config" in path
    admin_only = category in ("admin",) or "deep" in path or "config" in path

    auth_section = ""
    if auth_required:
        auth_section = textwrap.dedent(f"""\
            ## Authentication
            * **Required:** Yes
            * **Type:** Bearer JWT
            * **Header:** `Authorization: Bearer <token>`
            {"* **Role Required:** `admin`" if admin_only else "* **Role Required:** Any authenticated user"}
        """)

    sample_request = ""
    if method in ("POST", "PUT", "PATCH"):
        if "login" in path:
            sample_request = textwrap.dedent("""\
                ## Sample Request Body
                ```json
                {
                    "email": "engineer@nexusai.dev",
                    "password": "securePassword123"
                }
                ```
            """)
        elif "message" in path:
            sample_request = textwrap.dedent("""\
                ## Sample Request Body
                ```json
                {
                    "message": "How do I set up my VPN?"
                }
                ```
            """)
        elif "checklist" in path:
            sample_request = textwrap.dedent("""\
                ## Sample Request Body
                ```json
                {
                    "title": "Complete SSH key setup",
                    "description": "Generate ed25519 key and upload to GitHub",
                    "is_completed": false
                }
                ```
            """)
        else:
            sample_request = textwrap.dedent("""\
                ## Sample Request Body
                ```json
                {
                    "data": "See schema definition for field details."
                }
                ```
            """)

    return textwrap.dedent(f"""\
        # API Specification: {summary}

        ## Endpoint
        ```
        {method} {path}
        ```

        ## Description
        {description}

        ## Category
        `{category}`

        {auth_section}
        {sample_request}
        ## Response Codes
        | Status Code       | Description                              |
        |-------------------|------------------------------------------|
        | {success}         | Successful operation                     |
        | {error}           | Resource error or validation failure     |
        | 401 Unauthorized  | Missing or invalid JWT token             |
        | 403 Forbidden     | Insufficient role permissions             |
        | 500 Internal Error| Unexpected server error                  |

        ## Rate Limiting
        * **Limit:** {"60 req/min (unauthenticated)" if not auth_required else "200 req/min (authenticated)"}
        * **Headers:** `X-RateLimit-Remaining`, `X-RateLimit-Reset`

        ## Related Endpoints
        * See other `{category}` category endpoints in this folder.

        ---
        *API Documentation — {COMPANY} — Auto-generated v1 spec*
    """)


# ── B.2  MCP Tool Specifications (30 files) ──────────────────────────────────

MCP_TOOLS = [
    ("jira_create_issue",       "Jira",   "Creates a new issue in Jira Cloud.",
     {"project_key": "str", "summary": "str", "description": "str", "issue_type": "str (Task|Bug|Story)", "assignee_email": "str (optional)"},
     {"issue_key": "str", "url": "str", "status": "str"}),
    ("jira_get_issue",          "Jira",   "Retrieves a Jira issue by key.",
     {"issue_key": "str"}, {"key": "str", "summary": "str", "status": "str", "assignee": "str", "description": "str"}),
    ("jira_transition_issue",   "Jira",   "Transitions a Jira issue to a new status.",
     {"issue_key": "str", "target_status": "str (To Do|In Progress|Done)"}, {"success": "bool", "new_status": "str"}),
    ("jira_add_comment",        "Jira",   "Adds a comment to a Jira issue.",
     {"issue_key": "str", "body": "str"}, {"comment_id": "str", "created": "datetime"}),
    ("jira_get_sprint",         "Jira",   "Gets the active sprint for a board.",
     {"board_id": "int"}, {"sprint_id": "int", "name": "str", "start_date": "str", "end_date": "str", "issues": "list"}),
    ("jira_search_issues",      "Jira",   "Searches issues using JQL query.",
     {"jql": "str", "max_results": "int (default 50)"}, {"issues": "list[Issue]", "total": "int"}),
    ("jira_get_board",          "Jira",   "Gets board configuration and columns.",
     {"board_id": "int"}, {"id": "int", "name": "str", "type": "str", "columns": "list"}),
    ("jira_assign_issue",       "Jira",   "Assigns a Jira issue to a user.",
     {"issue_key": "str", "assignee_email": "str"}, {"success": "bool"}),
    ("jira_get_user_issues",    "Jira",   "Gets all issues assigned to a user.",
     {"email": "str", "status_filter": "str (optional)"}, {"issues": "list[Issue]"}),
    ("jira_create_sprint",      "Jira",   "Creates a new sprint on a board.",
     {"board_id": "int", "name": "str", "start_date": "str", "end_date": "str"}, {"sprint_id": "int", "state": "str"}),
    ("jira_get_velocity",       "Jira",   "Gets sprint velocity metrics.",
     {"board_id": "int", "num_sprints": "int (default 5)"}, {"sprints": "list", "avg_velocity": "float"}),
    ("jira_bulk_create",        "Jira",   "Creates multiple Jira issues in batch.",
     {"issues": "list[IssueInput]"}, {"created": "list[str]", "errors": "list"}),
    ("jira_get_changelog",      "Jira",   "Gets the change history for an issue.",
     {"issue_key": "str"}, {"changelog": "list[ChangeEntry]"}),
    ("jira_link_issues",        "Jira",   "Creates a link between two Jira issues.",
     {"inward_key": "str", "outward_key": "str", "link_type": "str"}, {"success": "bool"}),
    ("jira_get_priorities",     "Jira",   "Lists all available priority levels.",
     {}, {"priorities": "list[Priority]"}),
    ("github_list_repos",       "GitHub", "Lists repositories in the organization.",
     {"org": "str (default nexusai)"}, {"repos": "list[Repo]"}),
    ("github_get_repo",         "GitHub", "Gets repository details.",
     {"owner": "str", "repo": "str"}, {"name": "str", "description": "str", "default_branch": "str", "open_issues": "int"}),
    ("github_list_prs",         "GitHub", "Lists pull requests for a repository.",
     {"owner": "str", "repo": "str", "state": "str (open|closed|all)"}, {"pull_requests": "list[PR]"}),
    ("github_get_pr",           "GitHub", "Gets details of a specific pull request.",
     {"owner": "str", "repo": "str", "pr_number": "int"}, {"title": "str", "state": "str", "author": "str", "reviewers": "list", "diff_url": "str"}),
    ("github_create_pr",        "GitHub", "Creates a new pull request.",
     {"owner": "str", "repo": "str", "title": "str", "body": "str", "head": "str", "base": "str"}, {"pr_number": "int", "url": "str"}),
    ("github_list_branches",    "GitHub", "Lists branches in a repository.",
     {"owner": "str", "repo": "str"}, {"branches": "list[Branch]"}),
    ("github_get_file",         "GitHub", "Gets the content of a file from a repo.",
     {"owner": "str", "repo": "str", "path": "str", "ref": "str (optional)"}, {"content": "str", "sha": "str", "encoding": "str"}),
    ("github_search_code",      "GitHub", "Searches for code across repositories.",
     {"query": "str", "org": "str (optional)"}, {"results": "list[CodeResult]", "total": "int"}),
    ("github_list_commits",     "GitHub", "Lists recent commits on a branch.",
     {"owner": "str", "repo": "str", "branch": "str (optional)", "limit": "int (default 20)"}, {"commits": "list[Commit]"}),
    ("github_get_actions_runs", "GitHub", "Gets recent GitHub Actions workflow runs.",
     {"owner": "str", "repo": "str"}, {"runs": "list[WorkflowRun]"}),
    ("github_create_issue",     "GitHub", "Creates a new GitHub issue.",
     {"owner": "str", "repo": "str", "title": "str", "body": "str", "labels": "list[str]"}, {"issue_number": "int", "url": "str"}),
    ("github_get_issue",        "GitHub", "Gets a GitHub issue by number.",
     {"owner": "str", "repo": "str", "issue_number": "int"}, {"title": "str", "state": "str", "body": "str", "labels": "list"}),
    ("github_review_pr",        "GitHub", "Submits a review on a pull request.",
     {"owner": "str", "repo": "str", "pr_number": "int", "body": "str", "event": "str (APPROVE|REQUEST_CHANGES|COMMENT)"}, {"review_id": "int"}),
    ("github_merge_pr",         "GitHub", "Merges a pull request.",
     {"owner": "str", "repo": "str", "pr_number": "int", "merge_method": "str (squash|merge|rebase)"}, {"merged": "bool", "sha": "str"}),
    ("github_get_collaborators","GitHub", "Lists collaborators for a repository.",
     {"owner": "str", "repo": "str"}, {"collaborators": "list[User]"}),
]

def generate_mcp_spec(index: int, tool_name: str, integration: str,
                      description: str, input_schema: dict,
                      output_schema: dict) -> str:
    """Generate a realistic MCP tool specification markdown file."""
    input_table = "\n".join(
        f"    | `{k}` | `{v}` |"
        for k, v in input_schema.items()
    )
    output_table = "\n".join(
        f"    | `{k}` | `{v}` |"
        for k, v in output_schema.items()
    )

    input_json = "{\n" + ",\n".join(
        f'        "{k}": "<{v}>"' for k, v in input_schema.items()
    ) + "\n    }"

    output_json = "{\n" + ",\n".join(
        f'        "{k}": "<{v}>"' for k, v in output_schema.items()
    ) + "\n    }"

    error_scenarios = [
        ("401", "Authentication failed — invalid or expired PAT/API token."),
        ("403", "Insufficient permissions for the requested operation."),
        ("404", "Resource not found (invalid key, repo, or PR number)."),
        ("429", "Rate limit exceeded — retry after cooldown period."),
        ("500", "Internal server error on the external service."),
    ]
    selected_errors = random.sample(error_scenarios, k=random.randint(2, 4))
    error_rows = "\n".join(
        f"    | `{code}` | {desc} |" for code, desc in selected_errors
    )

    return textwrap.dedent(f"""\
        # MCP Tool Specification: `{tool_name}`

        ## Integration
        **{integration}** (via Model Context Protocol)

        ## Description
        {description}

        ## Tool Registration
        ```python
        @tool("{tool_name}")
        def {tool_name}(**kwargs) -> dict:
            \"\"\"{description}\"\"\"
            ...
        ```

        ## Input Schema
        | Parameter | Type |
        |-----------|------|
    {input_table}

        ### Example Input
        ```json
    {input_json}
        ```

        ## Output Schema
        | Field | Type |
        |-------|------|
    {output_table}

        ### Example Output
        ```json
    {output_json}
        ```

        ## Error Handling
        | Code | Description |
        |------|-------------|
    {error_rows}

        ## Usage Context
        This tool is invoked by the **Hermes Supervisor Agent** when the
        user's intent matches a `{integration.lower()}` operation. The
        agent orchestrator passes the structured arguments and receives
        the response for inclusion in the chat reply.

        ## Permissions
        * Requires a valid **{"Jira API Token" if integration == "Jira" else "GitHub Personal Access Token (PAT)"}** configured in the backend environment.
        * The token must have the following scopes:
        {"  * `read:jira-work`, `write:jira-work`" if integration == "Jira" else "  * `repo`, `read:org`, `workflow`"}

        ---
        *MCP Tool Documentation — {COMPANY} — Spec #{index:02d}*
    """)


# ═════════════════════════════════════════════════════════════════════════════
# SECTION C — MAIN EXECUTION
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Generate the complete synthetic knowledge base."""
    file_count = 0

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)

    # ── Write Core Dictionary Files ───────────────────────────────────────
    print("\n🔷 SECTION A: Writing core knowledge base files...\n")
    for rel_path, content in CORE_FILES.items():
        full_path = os.path.join(OUTPUT_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        file_count += 1
        print(f"  ✅ Created: {rel_path}")

    # ── Write Procedural API Spec Files ───────────────────────────────────
    print(f"\n🔷 SECTION B.1: Generating {len(API_ENDPOINTS)} API specification files...\n")
    api_dir = "07_api_specifications"
    for i, (method, path, summary, category, description) in enumerate(API_ENDPOINTS, 1):
        content = generate_api_spec(i, method, path, summary, category, description)
        filename = f"api_spec_v1_{i:02d}_{category}_{method.lower()}.md"
        rel_path = f"{api_dir}/{filename}"
        full_path = os.path.join(OUTPUT_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        file_count += 1
        print(f"  ✅ Created: {rel_path}")

    # ── Write Procedural MCP Tool Spec Files ──────────────────────────────
    print(f"\n🔷 SECTION B.2: Generating {len(MCP_TOOLS)} MCP tool specification files...\n")
    mcp_dir = "08_mcp_tool_specs"
    for i, (tool_name, integration, description, input_s, output_s) in enumerate(MCP_TOOLS, 1):
        content = generate_mcp_spec(i, tool_name, integration, description, input_s, output_s)
        filename = f"mcp_tool_spec_{i:02d}_{tool_name}.md"
        rel_path = f"{mcp_dir}/{filename}"
        full_path = os.path.join(OUTPUT_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        file_count += 1
        print(f"  ✅ Created: {rel_path}")

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"🎉 Knowledge base generation complete!")
    print(f"   📄 Total files generated: {file_count}")
    print(f"   📁 Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print(f"   📂 Categories:")

    # Count files per category
    for category_dir in sorted(os.listdir(OUTPUT_DIR)):
        cat_path = os.path.join(OUTPUT_DIR, category_dir)
        if os.path.isdir(cat_path):
            count = len([f for f in os.listdir(cat_path) if f.endswith(".md")])
            print(f"      └─ {category_dir}/ ({count} files)")

    print("=" * 60)


if __name__ == "__main__":
    main()
