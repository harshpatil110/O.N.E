# O.N.E — Onboarding Navigation Environment
## Semester 1 Task Breakdown — Full Detailed Task List

**Project:** Autonomous Developer Onboarding Agent (Capstone I)  
**Institute:** Vivekanand Education Society's Institute of Technology  
**Department:** Information Technology | Group No. 28  
**Guide:** Dr. Rakhi Jadhav  
**Team:** Archit Chitte, Parth Narkar, Harshvardhan Patil, Manas Patil  
**Stack:** Gemini 2.0 Flash · ChromaDB · FastAPI · React + Vite · PostgreSQL · Gmail SMTP

---

## Overview

This file contains the complete, highly detailed task breakdown for Semester 1 of the O.N.E project. The semester goal is to build a **fully functional MVP** — a working AI-powered developer onboarding chatbot with RAG knowledge retrieval, dynamic checklist generation, real-time progress tracking, and automated HR email notification.

All 22 tasks are organized across 6 sprints (weeks), matching the sprint plan in the technical document. Each task includes its purpose, every sub-step required to complete it, the files/modules to create, acceptance criteria, and dependencies on other tasks.

**Total Tasks: 22**  
**Duration: 6 Weeks**

---

## Sprint Map

| Sprint | Week | Tasks | Theme |
|--------|------|-------|-------|
| Sprint 1 | Week 1 | T-01 to T-04 | Foundation & Setup |
| Sprint 2 | Week 2 | T-05 to T-09 | Core AI Engine |
| Sprint 3 | Week 3 | T-10 to T-13 | RAG + Intelligence |
| Sprint 4 | Week 4 | T-14 to T-16 | Chat UI + Checklist |
| Sprint 5 | Week 5 | T-17 to T-19 | HR Notification + Dashboard |
| Sprint 6 | Week 6 | T-20 to T-22 | Testing, Polish, Demo Prep |

---

---

# SPRINT 1 — Foundation & Setup (Week 1)

---

## T-01 · Project Scaffolding and Repository Setup


**Dependencies:** None (first task)

### Purpose
Establish the complete project directory structure, version control setup, environment configuration, and inter-service communication conventions before any code is written. A clean scaffold prevents structural debt that causes refactoring pain later.

### Sub-tasks

#### 1.1 — Create GitHub Repository
- Create a new GitHub repository named `ONE-onboarding-agent`
- Set visibility to Private
- Initialize with a `README.md` that includes project name, description, team members, and tech stack
- Create two branches: `main` (production-ready) and `dev` (active development)
- Set branch protection on `main` — require pull request review before merging

#### 1.2 — Define Top-Level Directory Structure
Create the following folder layout at the repository root:
```
ONE-onboarding-agent/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   ├── agents/           # LLM agent logic
│   │   ├── rag/              # RAG pipeline
│   │   ├── services/         # Business logic (checklist, email, session)
│   │   ├── models/           # SQLAlchemy DB models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── core/             # Config, constants, FSM definitions
│   │   └── main.py           # FastAPI app entry point
│   ├── knowledge_base/       # Markdown documentation files
│   ├── chroma_db/            # ChromaDB persistent storage (gitignored)
│   ├── tests/                # pytest test files
│   ├── requirements.txt
│   └── .env.example
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page-level components (Chat, Dashboard, Login)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── api/              # Axios API call functions
│   │   ├── context/          # React context (auth, session)
│   │   └── main.jsx          # Vite entry point
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── docs/                     # Architecture diagrams, notes
├── .gitignore
└── README.md
```

#### 1.3 — Create `.gitignore`
Ensure the following are ignored:
- `__pycache__/`, `*.pyc`, `.pytest_cache/`
- `.env` files (never commit secrets)
- `backend/chroma_db/` (vector store is local, not committed)
- `node_modules/`
- `.DS_Store` (macOS)
- `*.egg-info/`
- `venv/`, `.venv/`

#### 1.4 — Backend Python Environment Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary \
            python-dotenv pydantic langchain langchain-google-genai \
            chromadb google-generativeai alembic httpx pytest pytest-asyncio
pip freeze > requirements.txt
```

#### 1.5 — Frontend Node Environment Setup
```bash
cd frontend
npm create vite@latest . -- --template react
npm install
npm install axios react-router-dom tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
Configure `tailwind.config.js` to scan `./src/**/*.{js,jsx}`.

#### 1.6 — Environment Variable Files
Create `backend/.env.example` with all required keys (no real values):
```
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/one_db

# JWT Auth
JWT_SECRET_KEY=your_jwt_secret_here
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=480

# Gmail SMTP
GMAIL_ADDRESS=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here

# HR Email (who receives completion reports)
HR_EMAIL=hr@company.com

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=one_knowledge_base

# App
APP_ENV=development
FRONTEND_URL=http://localhost:5173
```

Instruct all team members to copy this to `.env` and fill in real values locally.

#### 1.7 — FastAPI App Entry Point
Create `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="O.N.E API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "O.N.E Backend"}
```

Create `backend/app/core/config.py` using `pydantic_settings` to load `.env` variables.

#### 1.8 — Verify Everything Runs
- `cd backend && uvicorn app.main:app --reload` → visit `http://localhost:8000/health`
- `cd frontend && npm run dev` → visit `http://localhost:5173`
- Both should respond without errors

### Acceptance Criteria
- [ ] GitHub repo exists with `main` and `dev` branches
- [ ] Directory structure matches spec above
- [ ] `pip install -r requirements.txt` runs without errors
- [ ] `npm install` runs without errors
- [ ] FastAPI `/health` returns `{"status": "ok"}`
- [ ] React dev server runs at `localhost:5173` with default Vite page
- [ ] `.env` is in `.gitignore` and not committed
- [ ] `.env.example` is committed with all keys but no real values

---

## T-02 · PostgreSQL Database Schema Design and Setup

**Sprint:** 1 — Week 1  
**Estimated Effort:** 5–6 hours  
**Owner:** Backend team  
**Dependencies:** T-01

### Purpose
Design and implement the complete relational database schema that stores all onboarding sessions, checklist items, users, conversation logs, and knowledge base metadata. The schema must support all Semester 1 features and be extensible for Semester 2 additions.

### Sub-tasks

#### 2.1 — Install and Configure PostgreSQL Locally
- Install PostgreSQL (version 15+ recommended)
- Create a database: `CREATE DATABASE one_db;`
- Create a user: `CREATE USER one_user WITH PASSWORD 'yourpassword';`
- Grant privileges: `GRANT ALL PRIVILEGES ON DATABASE one_db TO one_user;`
- Update `DATABASE_URL` in `.env`: `postgresql://one_user:yourpassword@localhost:5432/one_db`

#### 2.2 — Define SQLAlchemy Models
Create `backend/app/models/` with the following files:

**`models/user.py`**
```python
# Fields: id (UUID, PK), name (str), email (str, unique), 
# hashed_password (str), role (enum: employee/hr_admin/eng_manager),
# created_at (datetime), is_active (bool)
```

**`models/onboarding_session.py`**
```python
# Fields: id (UUID, PK), user_id (UUID, FK → users.id),
# persona (JSONB) — stores full DeveloperPersona as JSON,
# status (enum: in_progress/completed/abandoned),
# current_fsm_state (str) — current state machine state,
# current_checklist_index (int, default 0),
# started_at (datetime, default now),
# completed_at (datetime, nullable),
# hr_notified (bool, default False),
# hr_notification_sent_at (datetime, nullable)
```

**`models/checklist_item.py`**
```python
# Fields: id (UUID, PK), session_id (UUID, FK → onboarding_sessions.id),
# item_key (str, 100) — unique key like "github_access",
# title (str, 500), description (text),
# category (enum: access/tooling/documentation/compliance/team),
# required (bool, default True),
# sort_order (int) — display order,
# applicable_roles (ARRAY of str), applicable_levels (ARRAY of str),
# applicable_stacks (ARRAY of str),
# knowledge_base_refs (ARRAY of str) — ChromaDB doc source paths,
# status (enum: pending/in_progress/completed/skipped, default pending),
# completed_at (datetime, nullable),
# notes (text, nullable) — agent/user notes about completion
```

**`models/conversation_log.py`**
```python
# Fields: id (UUID, PK), session_id (UUID, FK → onboarding_sessions.id),
# role (enum: user/assistant/system),
# content (text) — the message text,
# metadata (JSONB) — token counts, retrieval sources, tool calls used,
# created_at (datetime, default now)
```

**`models/checklist_template.py`**
```python
# Fields: id (UUID, PK), item_key (str, unique),
# title (str), description (text), category (enum),
# required (bool), sort_order (int),
# applicable_roles (ARRAY), applicable_levels (ARRAY),
# applicable_stacks (ARRAY), knowledge_base_refs (ARRAY),
# created_at (datetime), updated_at (datetime)
# This is the master template — sessions copy from here with persona filtering
```

#### 2.3 — Set Up Alembic for Migrations
```bash
cd backend
alembic init alembic
```
Configure `alembic.ini` to use `DATABASE_URL` from environment. Configure `alembic/env.py` to import all models so they are included in migrations.

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

#### 2.4 — Create Database Connection and Session
Create `backend/app/core/database.py`:
- SQLAlchemy `create_engine` using `DATABASE_URL`
- `SessionLocal` factory using `sessionmaker`
- `get_db()` dependency function for FastAPI dependency injection
- `Base = declarative_base()` imported by all models

#### 2.5 — Seed the Master Checklist Template
Create `backend/app/core/seed_data.py` — a script that populates `checklist_template` with 20+ pre-defined onboarding items covering all roles, levels, and stacks:

Example entries to include:
| item_key | title | category | required | applicable_roles | applicable_levels |
|---|---|---|---|---|---|
| github_access | GitHub org access and repo permissions | access | True | all | all |
| jira_access | Jira project board access | access | True | all | all |
| slack_access | Join Slack channels: #engineering, #backend, #incidents | access | True | all | all |
| local_dev_python | Local dev environment setup (Python 3.11, Poetry, Docker) | tooling | True | backend, fullstack, data | all |
| local_dev_node | Local dev environment setup (Node 20, npm, nvm) | tooling | True | frontend, fullstack | all |
| ide_setup | IDE setup with linting and formatting configs | tooling | False | all | all |
| read_architecture | Read Architecture Decision Records (ADRs) | documentation | True | all | mid, senior |
| read_api_guidelines | Review API design guidelines | documentation | True | backend, fullstack | all |
| read_deployment_runbook | Review deployment runbook | documentation | True | backend, devops, fullstack | all |
| read_git_workflow | Read intro to Git workflow and branching conventions | documentation | True | all | intern, junior |
| read_coding_standards | Review coding standards and code review process | documentation | True | all | all |
| sign_nda | Sign NDA and IP agreement | compliance | True | all | all |
| security_training | Complete security awareness training | compliance | True | all | all |
| meet_manager | Schedule 1:1 with engineering manager | team | True | all | all |
| buddy_session | Schedule buddy pairing session | team | True | all | all |
| cicd_setup | Review CI/CD pipeline documentation | documentation | True | devops, backend | all |
| docker_setup | Docker installation and local container setup | tooling | True | devops, backend, fullstack | all |
| python_venv | Set up Python virtual environment using Poetry | tooling | True | backend, data, fullstack | all |
| read_org_structure | Read org structure and team communication guidelines | documentation | False | all | intern |
| first_commit | Create a test branch and make a conventional commit | tooling | True | all | intern, junior |

Run this seed script once after migrations.

#### 2.6 — Verify Schema
- Run `alembic upgrade head` confirms no errors
- Connect to database and run `\dt` in psql to verify all tables exist
- Run seed script and verify `SELECT COUNT(*) FROM checklist_template;` returns 20+

### Acceptance Criteria
- [ ] PostgreSQL database `one_db` exists and is accessible
- [ ] All 5 tables created via Alembic migration
- [ ] Master checklist template seeded with 20+ items
- [ ] `get_db()` dependency works in a test FastAPI route
- [ ] All UUIDs use `gen_random_uuid()` as default
- [ ] JSONB columns work (insert and retrieve a persona object)

---

## T-03 · Knowledge Base Creation

**Sprint:** 1 — Week 1  
**Estimated Effort:** 6–8 hours  
**Owner:** All team members (content creation)  
**Dependencies:** T-01

### Purpose
Create the company knowledge base — the set of Markdown documents that the RAG system will retrieve from to answer developer questions. These documents simulate a real company's internal documentation and are the source of truth for the agent.

### Sub-tasks

#### 3.1 — Plan the Knowledge Base Structure
The knowledge base lives at `backend/knowledge_base/` with the following folder structure:
```
knowledge_base/
├── company/
│   ├── mission-and-values.md
│   ├── org-structure.md
│   └── communication-guidelines.md
├── engineering/
│   ├── architecture-overview.md
│   ├── coding-standards.md
│   ├── api-design-guidelines.md
│   ├── git-workflow.md
│   ├── code-review-process.md
│   └── adrs/
│       ├── adr-001-microservices.md
│       └── adr-002-event-driven.md
├── setup/
│   ├── local-dev-python.md
│   ├── local-dev-node.md
│   ├── docker-setup.md
│   └── ide-configuration.md
├── devops/
│   ├── ci-cd-pipeline.md
│   ├── deployment-runbook.md
│   └── monitoring-alerting.md
├── compliance/
│   ├── security-training.md
│   ├── data-handling-policy.md
│   └── nda-ip-agreement.md
└── team/
    ├── backend-team-intro.md
    ├── frontend-team-intro.md
    └── devops-team-intro.md
```

#### 3.2 — Write Key Documents (Content Requirements)
Each document must be substantive enough to be useful for RAG — minimum 300–500 words each. Key documents to write:

**`setup/local-dev-python.md`** — must include:
- Prerequisites (Python 3.11, pip)
- Installing Poetry: `pip install poetry`
- Creating a virtual environment: `poetry new project-name`
- Installing project dependencies: `poetry install`
- Activating the shell: `poetry shell`
- Running the dev server: `uvicorn app.main:app --reload`
- Environment variable setup instructions
- Common troubleshooting issues

**`setup/docker-setup.md`** — must include:
- Docker Desktop installation links (Mac, Windows, Linux)
- Verification: `docker --version && docker-compose --version`
- Minimum version requirements (Docker 24+, Compose v2+)
- Running the project with Docker Compose: `docker-compose up --build`
- Useful Docker commands for daily development
- How to stop all containers: `docker-compose down`

**`engineering/git-workflow.md`** — must include:
- Branch naming convention: `feat/`, `fix/`, `chore/`, `docs/`
- Conventional commit format: `feat(auth): add JWT token refresh`
- Pull request process: create PR → request review → get approval → merge
- Never commit directly to `main`
- Squash and merge policy
- Code owner review requirements

**`engineering/coding-standards.md`** — must include:
- Python: PEP 8, Black formatter, isort for imports
- JavaScript: ESLint + Prettier configuration
- Naming conventions (snake_case Python, camelCase JS)
- Comment and docstring requirements
- Maximum function length guideline

**`compliance/security-training.md`** — must include:
- Password policy (minimum 12 characters, no reuse)
- Multi-factor authentication requirement
- How to handle sensitive data and PII
- What to do if you suspect a security incident
- Acceptable use policy for company systems

**`compliance/nda-ip-agreement.md`** — must include:
- Summary of what the NDA covers
- IP assignment policy (work created for the company belongs to the company)
- What constitutes confidential information
- How to handle this document (who to contact to sign)

#### 3.3 — Add Document Metadata Headers
Every document must begin with a YAML front-matter block for metadata extraction during ingestion:
```yaml
---
title: "Local Development Setup - Python"
category: "setup"
applicable_roles: ["backend", "fullstack", "data"]
applicable_stacks: ["python"]
applicable_levels: ["intern", "junior", "mid", "senior"]
last_updated: "2026-01-01"
---
```

#### 3.4 — Knowledge Base README
Create `backend/knowledge_base/README.md` documenting:
- How to add a new document
- Required front-matter fields
- How to trigger re-ingestion into ChromaDB
- Document naming conventions

### Acceptance Criteria
- [ ] All 20+ markdown files exist in the correct folder structure
- [ ] Every file has valid YAML front-matter with all required fields
- [ ] Key documents (python setup, git workflow, coding standards, security) are substantive (300+ words)
- [ ] No placeholder text ("Lorem ipsum" or "TODO") in any document
- [ ] Knowledge base README exists

---

## T-04 · System Architecture Diagrams and API Contract

**Sprint:** 1 — Week 1  
**Estimated Effort:** 3–4 hours  
**Owner:** Tech lead  
**Dependencies:** T-01, T-02

### Purpose
Document the system architecture and define the API contract between frontend and backend before implementation begins. This prevents integration surprises mid-sprint and serves as the reference for the final report.

### Sub-tasks

#### 4.1 — Draw Architecture Diagrams
Create `docs/architecture/` and add the following diagrams (draw.io, Excalidraw, or Mermaid in Markdown):
- **System overview diagram** — shows all components (React frontend, FastAPI backend, Gemini API, ChromaDB, PostgreSQL, Gmail SMTP) and how they connect
- **Data flow diagram** — shows the path of a developer message from the browser through the agent, RAG retrieval, tool execution, and back to the browser
- **FSM state diagram** — shows all 7 states (WELCOME, PROFILING, PLAN_GENERATION, ONBOARDING_EXECUTION, CHECKLIST_REVIEW, COMPLETED, FREE_QA) and their transitions

#### 4.2 — Define Complete API Contract
Create `docs/api-contract.md` defining every endpoint with:
- HTTP method and path
- Request body schema (with example)
- Response schema (with example)
- Authentication requirement (public vs JWT required)
- Possible error responses

Endpoints to document (from the technical plan):
```
POST   /api/v1/auth/login
POST   /api/v1/auth/register-employee
POST   /api/v1/onboarding/start
GET    /api/v1/onboarding/{session_id}
GET    /api/v1/onboarding/{session_id}/progress
POST   /api/v1/chat/{session_id}/message
GET    /api/v1/chat/{session_id}/history
PATCH  /api/v1/checklist/{item_id}
GET    /api/v1/checklist/{session_id}
POST   /api/v1/knowledge/ingest
POST   /api/v1/knowledge/query
GET    /api/v1/admin/sessions
GET    /api/v1/admin/metrics
```

#### 4.3 — Define Pydantic Schemas
Create `backend/app/schemas/` with:
- `auth.py` — LoginRequest, TokenResponse, RegisterEmployeeRequest
- `session.py` — SessionResponse, StartSessionRequest, ProgressResponse
- `chat.py` — ChatMessageRequest, ChatMessageResponse
- `checklist.py` — ChecklistItemResponse, UpdateChecklistRequest
- `persona.py` — DeveloperPersona schema with all fields and enums

### Acceptance Criteria
- [ ] All three architecture diagrams exist in `docs/architecture/`
- [ ] `docs/api-contract.md` documents all 13 endpoints with request/response examples
- [ ] All Pydantic schemas created and importable
- [ ] Role and status enums defined and consistent across models and schemas

---

---

# SPRINT 2 — Core AI Engine (Week 2)

---

## T-05 · Gemini API Integration and LLM Client

**Sprint:** 2 — Week 2  
**Estimated Effort:** 4–5 hours  
**Owner:** AI/ML team member  
**Dependencies:** T-01, T-04

### Purpose
Set up the Google Gemini API client, test it works, and create a reusable LLM service wrapper that the rest of the backend uses for all model calls. This wrapper handles API key loading, error handling, retry logic for rate limit hits, and response parsing.

### Sub-tasks

#### 5.1 — Get Gemini API Key
- Go to `https://aistudio.google.com`
- Sign in with a Google account
- Click "Get API key" → "Create API key"
- Copy the key to `GEMINI_API_KEY` in `backend/.env`
- Verify the free tier limits: 15 requests/minute, 1500 requests/day

#### 5.2 — Test Gemini Connection
Create `backend/app/core/test_gemini.py` (a throw-away script):
```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("Say hello from O.N.E onboarding agent")
print(response.text)
```
Run it and confirm a response is printed.

#### 5.3 — Create LLM Service Class
Create `backend/app/services/llm_service.py`:

```python
class LLMService:
    def __init__(self):
        # Configure genai with API key from environment
        # Initialize GenerativeModel with "gemini-2.0-flash"
        # Set generation_config: temperature=0.3, max_output_tokens=2048
        pass

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        # Call model.generate_content with the prompt
        # Handle google.api_core.exceptions.ResourceExhausted (rate limit)
        # On rate limit: wait 4 seconds and retry up to 3 times
        # On other errors: raise a custom LLMError exception
        # Return response.text
        pass

    async def generate_with_tools(self, messages: list, tools: list, system_prompt: str) -> dict:
        # Call model.generate_content with tools parameter
        # Parse response for text vs function call parts
        # Return {"text": str, "tool_calls": list[{"name": str, "args": dict}]}
        pass

    async def extract_structured(self, prompt: str, output_schema: dict) -> dict:
        # Append instructions to respond only in JSON format
        # Call generate() and parse JSON from response
        # Handle JSON parse errors gracefully
        pass
```

#### 5.4 — Implement Rate Limit Retry Logic
```python
import asyncio
import json
import re

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 4

async def _call_with_retry(self, fn, *args, **kwargs):
    for attempt in range(MAX_RETRIES):
        try:
            return await fn(*args, **kwargs)
        except ResourceExhausted:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
            else:
                raise LLMRateLimitError("Gemini rate limit exceeded after retries")
```

#### 5.5 — Unit Test the LLM Service
Create `backend/tests/test_llm_service.py`:
- Test `generate()` returns a non-empty string
- Test `extract_structured()` returns a valid Python dict
- Test retry logic triggers correctly on rate limit (mock the API call)

### Acceptance Criteria
- [ ] Gemini API key configured and `.env` file updated
- [ ] `LLMService.generate()` works end-to-end (confirmed by running test script)
- [ ] `generate_with_tools()` correctly parses function call responses
- [ ] `extract_structured()` returns valid JSON-parsed dict
- [ ] Retry logic implemented and tested
- [ ] No API key hardcoded anywhere in source files

---

## T-06 · FSM (Finite State Machine) Implementation

**Sprint:** 2 — Week 2  
**Estimated Effort:** 4–5 hours  
**Owner:** Backend team  
**Dependencies:** T-02, T-05

### Purpose
Implement the Finite State Machine that governs the onboarding conversation flow. The FSM determines what the agent does at each point in the conversation — greeting, profiling, plan generation, task execution, review, and completion. It is the skeleton of the entire agent.

### Sub-tasks

#### 6.1 — Define FSM States and Transitions
Create `backend/app/core/fsm.py`:

```python
from enum import Enum

class FSMState(str, Enum):
    WELCOME = "WELCOME"
    PROFILING = "PROFILING"
    PLAN_GENERATION = "PLAN_GENERATION"
    ONBOARDING_EXECUTION = "ONBOARDING_EXECUTION"
    CHECKLIST_REVIEW = "CHECKLIST_REVIEW"
    COMPLETED = "COMPLETED"
    FREE_QA = "FREE_QA"   # overlay state — doesn't replace current state

# Valid transitions: {current_state: [allowed_next_states]}
VALID_TRANSITIONS = {
    FSMState.WELCOME: [FSMState.PROFILING],
    FSMState.PROFILING: [FSMState.PLAN_GENERATION],
    FSMState.PLAN_GENERATION: [FSMState.ONBOARDING_EXECUTION],
    FSMState.ONBOARDING_EXECUTION: [FSMState.CHECKLIST_REVIEW, FSMState.FREE_QA],
    FSMState.CHECKLIST_REVIEW: [FSMState.COMPLETED, FSMState.ONBOARDING_EXECUTION],
    FSMState.COMPLETED: [],
    FSMState.FREE_QA: [FSMState.ONBOARDING_EXECUTION, FSMState.CHECKLIST_REVIEW],
}
```

#### 6.2 — Implement FSM Controller
Create `backend/app/agents/fsm_controller.py`:

```python
class FSMController:
    def __init__(self, session_state: ConversationState):
        self.state = session_state

    def can_transition(self, to_state: FSMState) -> bool:
        # Check VALID_TRANSITIONS

    def transition(self, to_state: FSMState) -> None:
        # Validate transition, update self.state.current_fsm_state
        # Log the transition with timestamp

    def get_system_prompt_for_state(self) -> str:
        # Return state-specific system prompt
        # Each state has a different instruction set for the LLM
        pass

    def should_transition(self, agent_response: str, context: dict) -> FSMState | None:
        # Determine if a state transition is warranted based on:
        # - WELCOME: persona collected? → PROFILING
        # - PROFILING: all fields extracted? → PLAN_GENERATION
        # - PLAN_GENERATION: checklist saved? → ONBOARDING_EXECUTION
        # - ONBOARDING_EXECUTION: all required items done? → CHECKLIST_REVIEW
        # - CHECKLIST_REVIEW: user confirms complete? → COMPLETED
        pass
```

#### 6.3 — Define System Prompts Per State
Create `backend/app/core/prompts.py` with system prompt templates for each FSM state:

**WELCOME prompt:**
```
You are O.N.E — the Onboarding Navigation Environment, an AI assistant helping new developers join the team.
Your job right now is to warmly greet the new developer and collect their name, email address, and start date.
Be friendly, professional, and concise. Once you have their name and email, confirm and move on.
```

**PROFILING prompt:**
```
You are O.N.E, a developer onboarding assistant. You are now profiling the new developer.
Ask the following questions conversationally (not as a form):
1. What role are you joining as? (backend / frontend / devops / fullstack / data)
2. How would you describe your experience level? (intern / junior / mid / senior)
3. What is your primary technology stack? (e.g. Python, Node.js, Go)
4. Which team are you joining?
Extract structured data from their natural language responses.
```

**ONBOARDING_EXECUTION prompt:**
```
You are O.N.E, guiding {developer_name} ({role}, {experience_level}) through onboarding.
Current task: {current_task_title} — {current_task_description}
Category: {category}

Guide the developer through completing this task. Reference the documentation provided below.
When the developer confirms completion, call the mark_checklist_item tool with status="completed".
Only use information from the provided documentation — never make up URLs, credentials, or tool names.
If you don't know something, say so and suggest they ask in #engineering-help on Slack.

[Source documents are appended here by the RAG pipeline]
```

**CHECKLIST_REVIEW prompt:**
```
You are O.N.E. The developer has completed their onboarding checklist.
Show them a summary of completed and pending items.
Ask: "You have completed X of Y required tasks. Shall I send your completion report to HR?"
Wait for confirmation before calling the send_hr_completion_email tool.
```

#### 6.4 — ConversationState Model
Create `backend/app/core/state.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ConversationState:
    session_id: str
    user_id: str
    current_fsm_state: FSMState = FSMState.WELCOME
    persona: dict = field(default_factory=dict)
    checklist: list = field(default_factory=list)
    current_checklist_index: int = 0
    conversation_history: list = field(default_factory=list)  # last 20 messages
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
```

### Acceptance Criteria
- [ ] All 7 FSM states defined as enum
- [ ] `can_transition()` correctly validates allowed transitions
- [ ] `transition()` raises `InvalidTransitionError` for invalid moves
- [ ] System prompts exist for all states (WELCOME, PROFILING, PLAN_GENERATION, ONBOARDING_EXECUTION, CHECKLIST_REVIEW, COMPLETED)
- [ ] `ConversationState` dataclass is importable and serializable to dict
- [ ] Unit tests cover all valid and invalid state transitions

---

## T-07 · Persona Detection Agent

**Sprint:** 2 — Week 2  
**Estimated Effort:** 5–6 hours  
**Owner:** AI/ML team member  
**Dependencies:** T-05, T-06

### Purpose
Implement the persona extraction logic. When a developer types "I'm a senior backend dev mostly in Python and Go", the system must convert that into the structured `DeveloperPersona` object. This extraction uses Gemini with a structured output prompt — not regex or keyword matching.

### Sub-tasks

#### 7.1 — Define DeveloperPersona Pydantic Model
In `backend/app/schemas/persona.py`:
```python
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import date

class DeveloperPersona(BaseModel):
    name: str
    email: str
    start_date: Optional[date] = None
    role: Literal["backend", "frontend", "devops", "fullstack", "data"]
    experience_level: Literal["intern", "junior", "mid", "senior"]
    tech_stack: List[str]  # e.g. ["python", "django", "postgres"]
    team: Optional[str] = None
    
    def is_complete(self) -> bool:
        return all([self.name, self.email, self.role, 
                    self.experience_level, self.tech_stack])
```

#### 7.2 — Implement Persona Extraction Function
Create `backend/app/agents/persona_agent.py`:

```python
PERSONA_EXTRACTION_PROMPT = """
You are extracting a structured developer profile from a conversation.

Given the conversation history below, extract the following fields:
- name: the developer's full name
- email: their email address  
- role: one of [backend, frontend, devops, fullstack, data]
- experience_level: one of [intern, junior, mid, senior]
- tech_stack: a list of technologies (e.g. ["python", "fastapi", "postgres"])
- team: their team name if mentioned, or null

Map natural language to the correct enum values:
- "backend developer", "backend engineer", "server side" → "backend"
- "frontend dev", "UI developer", "React developer" → "frontend"
- "DevOps", "SRE", "infrastructure engineer" → "devops"
- "full stack", "full-stack" → "fullstack"
- "data engineer", "ML engineer", "data scientist" → "data"
- "intern", "trainee" → "intern"
- "junior", "entry level", "1-2 years" → "junior"
- "mid level", "mid-level", "3-5 years" → "mid"
- "senior", "lead", "staff", "principal" → "senior"

Return ONLY a JSON object with these exact keys. No explanation text.
If a field is not yet available, set it to null.

Conversation history:
{conversation_history}
"""

class PersonaAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def extract_persona(self, conversation_history: list) -> dict:
        # Format conversation history as readable text
        # Call llm.extract_structured with PERSONA_EXTRACTION_PROMPT
        # Validate result against DeveloperPersona fields
        # Return partial persona dict (may have nulls if not collected yet)
        pass

    async def check_profiling_complete(self, persona: dict) -> bool:
        # Check if all required fields are non-null
        # Required: name, email, role, experience_level, tech_stack
        pass

    async def get_next_profiling_question(self, persona: dict) -> str:
        # Return the next question to ask based on what's missing
        # If name missing: "What's your name and email address?"
        # If role missing: "What role are you joining as?"
        # If experience_level missing: "How would you describe your experience level?"
        # If tech_stack missing: "What's your primary tech stack?"
        # If team missing: "Which team are you joining?"
        pass
```

#### 7.3 — Test Persona Extraction
Create test cases in `backend/tests/test_persona_agent.py`:

```python
test_cases = [
    {
        "input": "Hi I'm Jane Doe, jane@company.com. I'm a senior backend developer mostly working with Python and Go.",
        "expected": {
            "name": "Jane Doe",
            "email": "jane@company.com",
            "role": "backend",
            "experience_level": "senior",
            "tech_stack": ["python", "go"]
        }
    },
    {
        "input": "I'm Alex, alex@company.com, a junior frontend dev. I mainly use React and TypeScript.",
        "expected": {
            "name": "Alex",
            "role": "frontend",
            "experience_level": "junior",
            "tech_stack": ["react", "typescript"]
        }
    },
    {
        "input": "Intern here! My name is Rahul Sharma, rahul@company.com. I'm just starting out with Python.",
        "expected": {
            "name": "Rahul Sharma",
            "role": "backend",
            "experience_level": "intern",
            "tech_stack": ["python"]
        }
    }
]
```

Run all test cases and verify extraction accuracy.

### Acceptance Criteria
- [ ] `extract_persona()` correctly extracts all fields from natural language in 3+ test cases
- [ ] Role and experience enums are mapped correctly from synonyms
- [ ] `is_complete()` returns False when required fields are missing
- [ ] `get_next_profiling_question()` returns the correct next question based on what is missing
- [ ] Extraction uses LLM structured output, not hardcoded keyword matching

---

## T-08 · Dynamic Checklist Generator

**Sprint:** 2 — Week 2  
**Estimated Effort:** 5–6 hours  
**Owner:** Backend team  
**Dependencies:** T-02, T-07

### Purpose
Given a completed `DeveloperPersona`, generate a personalised onboarding checklist by filtering the master template. A senior Python backend developer should get a different set of tasks than an intern frontend developer. This is the core personalisation logic of the system.

### Sub-tasks

#### 8.1 — Implement Checklist Generator Service
Create `backend/app/services/checklist_service.py`:

```python
class ChecklistService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_checklist_for_persona(
        self, session_id: str, persona: DeveloperPersona
    ) -> List[ChecklistItem]:
        """
        Algorithm:
        1. Load ALL items from checklist_template table
        2. Filter: keep item if persona.role in item.applicable_roles OR "all" in item.applicable_roles
        3. Filter: keep item if persona.experience_level in item.applicable_levels OR "all" in item.applicable_levels
        4. Filter: keep item if any tech in persona.tech_stack is in item.applicable_stacks OR "all" in item.applicable_stacks
        5. Sort by item.sort_order
        6. Create ChecklistItem rows in DB for this session_id
        7. Return list of created ChecklistItem objects
        """
        pass

    async def get_checklist(self, session_id: str) -> List[ChecklistItem]:
        # Query checklist_items where session_id = session_id, order by sort_order
        pass

    async def get_current_item(self, session_id: str) -> ChecklistItem | None:
        # Get first item with status=pending or status=in_progress
        pass

    async def update_item_status(
        self, item_id: str, status: str, notes: str = None
    ) -> ChecklistItem:
        # Update status and optionally notes
        # If status=completed, set completed_at=datetime.utcnow()
        pass

    async def get_progress(self, session_id: str) -> dict:
        # Count completed, pending, skipped, total items
        # Calculate percent_complete
        # Return progress dict matching the API response schema
        pass

    async def all_required_complete(self, session_id: str) -> bool:
        # Check if all items where required=True have status=completed
        pass
```

#### 8.2 — Filtering Logic Test Cases
Write test cases in `backend/tests/test_checklist_service.py`:

**Senior Backend Python developer should receive:**
- github_access ✓ (all roles)
- local_dev_python ✓ (backend/fullstack/data roles)
- local_dev_node ✗ (frontend/fullstack only — NOT backend)
- read_architecture ✓ (mid/senior levels)
- read_git_workflow ✗ (intern/junior only — NOT senior)
- sign_nda ✓ (all roles, all levels)
- docker_setup ✓ (devops/backend/fullstack)

**Intern Frontend Node developer should receive:**
- github_access ✓
- local_dev_node ✓ (frontend role)
- local_dev_python ✗ (backend/data only)
- read_git_workflow ✓ (intern/junior)
- read_architecture ✗ (mid/senior only)
- ide_setup ✓ (all roles — though not required)

#### 8.3 — Save Checklist to Database
After filtering, create `ChecklistItem` rows in the database for the session:
```python
for idx, template_item in enumerate(filtered_items):
    checklist_item = ChecklistItem(
        session_id=session_id,
        item_key=template_item.item_key,
        title=template_item.title,
        description=template_item.description,
        category=template_item.category,
        required=template_item.required,
        sort_order=idx,
        applicable_roles=template_item.applicable_roles,
        applicable_levels=template_item.applicable_levels,
        applicable_stacks=template_item.applicable_stacks,
        knowledge_base_refs=template_item.knowledge_base_refs,
        status="pending"
    )
    self.db.add(checklist_item)
self.db.commit()
```

### Acceptance Criteria
- [ ] `generate_checklist_for_persona()` filters correctly for 4 different persona combinations
- [ ] Filtered checklist items are saved to the `checklist_items` table
- [ ] `get_progress()` returns correct counts and percentage
- [ ] `all_required_complete()` returns True only when all required items are done
- [ ] `update_item_status()` sets `completed_at` when status is "completed"
- [ ] Checklist for intern has more items than for senior (more hand-holding tasks)

---

## T-09 · Core Agent Orchestrator and Message Handler

**Sprint:** 2 — Week 2  
**Estimated Effort:** 6–7 hours  
**Owner:** AI/ML + Backend team  
**Dependencies:** T-05, T-06, T-07, T-08

### Purpose
Build the central `AgentOrchestrator` that handles every incoming developer message. This is the brain that decides: load state → classify intent → retrieve RAG context if needed → build prompt → call Gemini → execute tool calls → update state → return response.

### Sub-tasks

#### 9.1 — Define Agent Tools
Create `backend/app/agents/tools.py`:

```python
AGENT_TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "Search the company knowledge base for relevant documentation to answer developer questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "category": {
                    "type": "string",
                    "enum": ["setup", "engineering", "compliance", "team", "company", "devops"],
                    "description": "Optional: filter by document category"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "mark_checklist_item",
        "description": "Update the status of a checklist item when a developer completes, starts, or skips it.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {"type": "string"},
                "status": {"type": "string", "enum": ["completed", "in_progress", "skipped"]},
                "notes": {"type": "string", "description": "Optional notes about completion"}
            },
            "required": ["item_id", "status"]
        }
    },
    {
        "name": "get_checklist_status",
        "description": "Get the current checklist with all item statuses and progress percentage.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "send_hr_completion_email",
        "description": "Send the onboarding completion report to HR. Only call this after all required items are done AND the developer has confirmed they want to complete.",
        "parameters": {
            "type": "object",
            "properties": {
                "include_pending": {"type": "boolean", "description": "Include pending/skipped items in the report"}
            },
            "required": ["include_pending"]
        }
    },
    {
        "name": "escalate_to_human",
        "description": "Escalate to a human buddy or manager when the agent cannot answer a question.",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"},
                "channel": {"type": "string", "enum": ["email"]}
            },
            "required": ["reason", "channel"]
        }
    }
]
```

#### 9.2 — Implement Agent Orchestrator
Create `backend/app/agents/orchestrator.py`:

```python
class AgentOrchestrator:
    def __init__(self, session_id: str, db: Session):
        self.session_id = session_id
        self.db = db
        self.llm = LLMService()
        self.rag = RAGService()
        self.checklist_service = ChecklistService(db)
        self.fsm = None  # loaded from DB state

    async def load_or_create_state(self) -> ConversationState:
        # Load session from DB
        # Reconstruct ConversationState from DB session + conversation_log
        # Load last 20 messages from conversation_log
        pass

    async def handle_message(self, user_message: str) -> str:
        # 1. Load state
        state = await self.load_or_create_state()
        self.fsm = FSMController(state)

        # 2. Classify intent
        intent = await self._classify_intent(user_message)
        
        # 3. Retrieve RAG context if needed
        context_docs = []
        if intent in ["question", "task_help"]:
            current_item = await self.checklist_service.get_current_item(self.session_id)
            context_docs = await self.rag.retrieve(
                query=user_message,
                role=state.persona.get("role"),
                tech_stack=state.persona.get("tech_stack", []),
                checklist_item=current_item
            )

        # 4. Build system prompt for current FSM state
        system_prompt = self.fsm.get_system_prompt_for_state()
        if context_docs:
            system_prompt += self._format_context_docs(context_docs)

        # 5. Append user message to history
        state.conversation_history.append({"role": "user", "content": user_message})
        # Keep only last 20 messages
        state.conversation_history = state.conversation_history[-20:]

        # 6. Call LLM with tools
        response = await self.llm.generate_with_tools(
            messages=state.conversation_history,
            tools=AGENT_TOOLS,
            system_prompt=system_prompt
        )

        # 7. Execute tool calls if any
        while response.get("tool_calls"):
            for tool_call in response["tool_calls"]:
                tool_result = await self._execute_tool(tool_call, state)
                # Add tool result to message history for LLM to see
                state.conversation_history.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_name": tool_call["name"]
                })
            # Continue LLM call with tool results
            response = await self.llm.generate_with_tools(
                messages=state.conversation_history,
                tools=AGENT_TOOLS,
                system_prompt=system_prompt
            )

        assistant_reply = response["text"]

        # 8. Check for FSM state transition
        next_state = self.fsm.should_transition(assistant_reply, {"persona": state.persona})
        if next_state:
            self.fsm.transition(next_state)

        # 9. Append assistant response to history
        state.conversation_history.append({"role": "assistant", "content": assistant_reply})

        # 10. Persist to DB
        await self._persist_state(state, user_message, assistant_reply)

        return assistant_reply

    async def _classify_intent(self, message: str) -> str:
        # Use LLM to classify: "question", "task_completion", "task_help", "chitchat", "skip_request"
        # This is a cheap call — short prompt, no tools
        pass

    async def _execute_tool(self, tool_call: dict, state: ConversationState) -> dict:
        name = tool_call["name"]
        args = tool_call.get("args", {})
        
        if name == "search_knowledge_base":
            return await self.rag.retrieve(query=args["query"], category=args.get("category"))
        elif name == "mark_checklist_item":
            return await self.checklist_service.update_item_status(
                item_id=args["item_id"], status=args["status"], notes=args.get("notes")
            )
        elif name == "get_checklist_status":
            return await self.checklist_service.get_progress(self.session_id)
        elif name == "send_hr_completion_email":
            return await self._trigger_hr_email(state, args["include_pending"])
        elif name == "escalate_to_human":
            return await self._handle_escalation(args["reason"])
        
        return {"error": f"Unknown tool: {name}"}

    async def _persist_state(self, state, user_message, assistant_reply):
        # Save user message to conversation_logs
        # Save assistant reply to conversation_logs
        # Update onboarding_session: current_fsm_state, current_checklist_index, last_active
        pass
```

#### 9.3 — Implement the Chat API Endpoint
In `backend/app/api/chat.py`:
```python
@router.post("/chat/{session_id}/message", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orchestrator = AgentOrchestrator(session_id=session_id, db=db)
    reply = await orchestrator.handle_message(request.message)
    return ChatMessageResponse(reply=reply, session_id=session_id)
```

### Acceptance Criteria
- [ ] `handle_message()` returns a non-empty string response for any input
- [ ] FSM transitions correctly as conversation progresses
- [ ] Tool calls are executed and results fed back to the LLM
- [ ] Conversation history is limited to 20 messages
- [ ] State is persisted to DB after every message
- [ ] Chat API endpoint returns 200 with reply text

---

---

# SPRINT 3 — RAG + Intelligence (Week 3)

---

## T-10 · ChromaDB Setup and Document Ingestion Pipeline

**Sprint:** 3 — Week 3  
**Estimated Effort:** 5–6 hours  
**Owner:** AI/ML team member  
**Dependencies:** T-03, T-05

### Purpose
Set up ChromaDB as the local vector database and build the ingestion pipeline that processes all knowledge base documents into searchable embeddings. This is the foundation of the RAG system.

### Sub-tasks

#### 10.1 — Initialize ChromaDB Client
Create `backend/app/rag/chroma_client.py`:
```python
import chromadb
from chromadb.config import Settings
import os

def get_chroma_client():
    return chromadb.PersistentClient(
        path=os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db"),
        settings=Settings(anonymized_telemetry=False)
    )

def get_collection(client=None):
    if client is None:
        client = get_chroma_client()
    return client.get_or_create_collection(
        name=os.getenv("CHROMA_COLLECTION_NAME", "one_knowledge_base"),
        metadata={"hnsw:space": "cosine"}
    )
```

The `PersistentClient` saves embeddings to disk in the `chroma_db/` folder — no separate server needed.

#### 10.2 — Implement Gemini Embedding Function
Create `backend/app/rag/embeddings.py`:
```python
import google.generativeai as genai

class GeminiEmbeddingFunction:
    """ChromaDB-compatible embedding function using Gemini text-embedding-004."""

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "models/text-embedding-004"

    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings = []
        for text in input:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result["embedding"])
        return embeddings
```

Note: `text-embedding-004` produces 768-dimensional vectors and is free within the Gemini API free tier.

#### 10.3 — Build Document Loader
Create `backend/app/rag/document_loader.py`:
```python
import os
import re
import yaml

def load_knowledge_base(kb_directory: str) -> list[dict]:
    """
    Walk the knowledge_base/ directory, read all .md files,
    parse YAML front-matter, and return list of document dicts.
    
    Each returned dict:
    {
        "content": "...body text without front-matter...",
        "metadata": {
            "source": "setup/local-dev-python.md",
            "title": "Local Development Setup - Python",
            "category": "setup",
            "applicable_roles": ["backend", "fullstack", "data"],
            "applicable_stacks": ["python"],
            "applicable_levels": ["intern", "junior", "mid", "senior"]
        }
    }
    """
    documents = []
    for root, dirs, files in os.walk(kb_directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, kb_directory)
                content, metadata = parse_markdown_file(filepath, relative_path)
                if content:
                    documents.append({"content": content, "metadata": metadata})
    return documents

def parse_markdown_file(filepath: str, relative_path: str) -> tuple:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    # Extract YAML front-matter between --- delimiters
    # Strip front-matter from content
    # Return (content_text, metadata_dict)
    pass
```

#### 10.4 — Build Text Chunker
Create `backend/app/rag/chunker.py`:
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Split each document into chunks of ~512 tokens with 50-token overlap.
    Preserve metadata from parent document in each chunk.
    Each chunk gets a unique ID: "{source}:chunk_{n}"
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,     # ~512 tokens at ~4 chars/token
        chunk_overlap=200,   # ~50 tokens overlap
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
        # Split on headings first to preserve section coherence
    )
    chunks = []
    for doc in documents:
        texts = splitter.split_text(doc["content"])
        for i, text in enumerate(texts):
            chunks.append({
                "id": f"{doc['metadata']['source']}:chunk_{i}",
                "content": text,
                "metadata": {**doc["metadata"], "chunk_index": i}
            })
    return chunks
```

#### 10.5 — Build Ingestion Script
Create `backend/app/rag/ingest.py`:
```python
async def ingest_knowledge_base(kb_directory: str = None):
    """
    Full ingestion pipeline:
    1. Load all documents from knowledge_base/
    2. Chunk them
    3. Generate embeddings via Gemini
    4. Store in ChromaDB
    
    Idempotent: clears existing collection and rebuilds from scratch.
    """
    if kb_directory is None:
        kb_directory = os.path.join(os.path.dirname(__file__), "../../knowledge_base")
    
    print("Loading documents...")
    documents = load_knowledge_base(kb_directory)
    print(f"Loaded {len(documents)} documents")
    
    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    print("Storing in ChromaDB...")
    collection = get_collection()
    embedding_fn = GeminiEmbeddingFunction()
    
    # Process in batches of 10 to respect rate limits
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        collection.upsert(
            ids=[c["id"] for c in batch],
            documents=[c["content"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
            embeddings=embedding_fn([c["content"] for c in batch])
        )
        print(f"  Ingested batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
    
    print(f"Ingestion complete. Total chunks in collection: {collection.count()}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(ingest_knowledge_base())
```

Run this script after creating the knowledge base: `python -m app.rag.ingest`

#### 10.6 — Add Admin Ingestion Endpoint
In `backend/app/api/knowledge.py`:
```python
@router.post("/knowledge/ingest")
async def trigger_ingestion(current_user: User = Depends(get_admin_user)):
    await ingest_knowledge_base()
    return {"status": "ingestion complete"}
```

### Acceptance Criteria
- [ ] ChromaDB collection created and persisted to `chroma_db/` folder on disk
- [ ] Ingestion script processes all 20+ markdown files without errors
- [ ] `collection.count()` returns 50+ chunks after ingestion
- [ ] Each chunk has correct metadata fields (source, category, applicable_roles, etc.)
- [ ] Embeddings are 768-dimensional (Gemini text-embedding-004)
- [ ] Ingestion is idempotent — running it twice doesn't duplicate chunks

---

## T-11 · RAG Retrieval Service

**Sprint:** 3 — Week 3  
**Estimated Effort:** 5–6 hours  
**Owner:** AI/ML team member  
**Dependencies:** T-10

### Purpose
Build the retrieval service that, given a developer's question and their persona, finds the most relevant documentation chunks from ChromaDB. This service handles metadata filtering, semantic similarity search, and result formatting for injection into the LLM prompt.

### Sub-tasks

#### 11.1 — Implement Query Embedding Function
In `backend/app/rag/embeddings.py`, add a query embedding function:
```python
def embed_query(text: str) -> list[float]:
    """Embed a query string using RETRIEVAL_QUERY task type."""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"  # Different task type for queries vs documents
    )
    return result["embedding"]
```

Note: Gemini requires different `task_type` for document embeddings (`retrieval_document`) vs query embeddings (`retrieval_query`). Using the wrong task type degrades retrieval quality significantly.

#### 11.2 — Implement RAG Service
Create `backend/app/rag/rag_service.py`:

```python
class RAGService:
    def __init__(self):
        self.collection = get_collection()

    async def retrieve(
        self,
        query: str,
        role: str = None,
        tech_stack: list = None,
        checklist_item=None,
        category: str = None,
        top_k: int = 3
    ) -> list[dict]:
        """
        Retrieval strategy:
        1. Build metadata filter from persona (role, tech_stack)
        2. If checklist_item has knowledge_base_refs, add source filter
        3. Run ChromaDB similarity search (top 10 candidates)
        4. Re-rank with LLM to select top 3
        5. Return formatted list of document dicts
        """
        
        # 1. Build where clause for ChromaDB metadata filter
        where_conditions = []
        if role:
            where_conditions.append({"applicable_roles": {"$contains": role}})
        if category:
            where_conditions.append({"category": {"$eq": category}})
        
        where = {"$and": where_conditions} if len(where_conditions) > 1 \
                else where_conditions[0] if where_conditions else None
        
        # 2. Embed the query
        query_embedding = embed_query(query)
        
        # 3. Semantic search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(10, self.collection.count()),
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        # 4. Format results
        documents = []
        if results["documents"] and results["documents"][0]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            ):
                documents.append({
                    "content": doc,
                    "source": meta.get("source", "unknown"),
                    "title": meta.get("title", ""),
                    "category": meta.get("category", ""),
                    "similarity_score": 1 - dist  # convert distance to similarity
                })
        
        # 5. Filter by confidence threshold — don't include very low-relevance docs
        documents = [d for d in documents if d["similarity_score"] >= 0.4]
        
        # 6. Return top_k results
        return documents[:top_k]

    def format_for_prompt(self, documents: list[dict]) -> str:
        """Format retrieved documents for injection into LLM system prompt."""
        if not documents:
            return ""
        
        formatted = "\n\n--- RETRIEVED DOCUMENTATION ---\n"
        for doc in documents:
            formatted += f"\n[Source: {doc['source']}]\n{doc['content']}\n"
        formatted += "\n--- END OF DOCUMENTATION ---\n"
        return formatted
```

#### 11.3 — Add Source Citation Logic
When the agent uses retrieved documents, the response must include source citations. Add to the ONBOARDING_EXECUTION system prompt:
```
When answering using the provided documentation, always end your answer with:
"[Source: {filename}]"
If you use multiple sources, cite all of them.
If the information is not in the provided documentation, say:
"I don't have information about that in our knowledge base. Please reach out to #engineering-help on Slack."
```

#### 11.4 — Add Direct RAG Query Endpoint (for Testing)
In `backend/app/api/knowledge.py`:
```python
@router.post("/knowledge/query")
async def query_knowledge_base(
    request: KnowledgeQueryRequest,
    current_user: User = Depends(get_current_user)
):
    rag = RAGService()
    results = await rag.retrieve(
        query=request.query,
        role=request.role,
        category=request.category
    )
    return {"query": request.query, "results": results}
```

This endpoint allows manual testing of the RAG pipeline during development.

#### 11.5 — RAG Retrieval Test Cases
Create `backend/tests/test_rag_service.py` with at least 5 test queries:
```python
test_queries = [
    {
        "query": "How do I install Python 3.11?",
        "expected_source_contains": "local-dev-python",
        "role": "backend"
    },
    {
        "query": "What is the branch naming convention?",
        "expected_source_contains": "git-workflow",
        "role": "backend"
    },
    {
        "query": "What does the NDA cover?",
        "expected_source_contains": "nda-ip-agreement",
        "role": "backend"
    },
    {
        "query": "How do I run the project with Docker?",
        "expected_source_contains": "docker-setup",
        "role": "devops"
    },
    {
        "query": "What are the code review requirements?",
        "expected_source_contains": "code-review-process",
        "role": "backend"
    }
]
```

### Acceptance Criteria
- [ ] `retrieve()` returns 1-3 relevant documents for all 5 test queries
- [ ] Metadata filtering by role reduces irrelevant results
- [ ] Similarity score below 0.4 is filtered out (prevents garbage results)
- [ ] `format_for_prompt()` produces clean, readable context for LLM injection
- [ ] `/api/v1/knowledge/query` endpoint works and returns results
- [ ] Source citations appear in agent responses when RAG is used

---

## T-12 · Authentication System (JWT)

**Sprint:** 3 — Week 3  
**Estimated Effort:** 4–5 hours  
**Owner:** Backend team  
**Dependencies:** T-02, T-04

### Purpose
Implement JWT-based authentication so that only registered employees can access the chat API, and only HR admins can access the admin dashboard endpoints. Without auth, anyone with the API URL could start an onboarding session.

### Sub-tasks

#### 12.1 — Implement Password Hashing
In `backend/app/core/security.py`:
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=480))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
```

Add `passlib[bcrypt]` and `python-jose[cryptography]` to `requirements.txt`.

#### 12.2 — Implement Auth Endpoints
In `backend/app/api/auth.py`:
```python
@router.post("/auth/register-employee", response_model=UserResponse)
async def register_employee(
    request: RegisterEmployeeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hr_admin_user)  # only HR admin can register
):
    # Check email not already registered
    # Hash password
    # Create user with role="employee"
    # Return user response (no password)
    pass

@router.post("/auth/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    # Find user by email
    # Verify password
    # Create JWT token with user_id and role in payload
    # Return {"access_token": token, "token_type": "bearer", "role": user.role}
    pass
```

#### 12.3 — Implement JWT Dependency
Create `backend/app/core/auth_deps.py`:
```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Decode JWT, extract user_id
    # Load user from DB
    # Return user or raise 401

async def get_hr_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["hr_admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="HR admin access required")
    return current_user
```

#### 12.4 — Seed Test Users
Add to `seed_data.py`:
```python
def seed_users(db):
    # Create one HR admin user
    hr_admin = User(
        name="HR Admin",
        email="hr@company.com",
        hashed_password=hash_password("adminpassword123"),
        role="hr_admin"
    )
    # Create one test employee
    employee = User(
        name="Test Developer",
        email="dev@company.com",
        hashed_password=hash_password("devpassword123"),
        role="employee"
    )
    db.add_all([hr_admin, employee])
    db.commit()
```

### Acceptance Criteria
- [ ] `POST /api/v1/auth/login` returns JWT token for valid credentials
- [ ] `POST /api/v1/auth/login` returns 401 for invalid password
- [ ] Protected endpoints return 401 without a valid token
- [ ] Admin endpoints return 403 for employee role
- [ ] Passwords are stored as bcrypt hashes (never plaintext)

---

## T-13 · Onboarding Session Management API

**Sprint:** 3 — Week 3  
**Estimated Effort:** 4–5 hours  
**Owner:** Backend team  
**Dependencies:** T-02, T-08, T-12

### Purpose
Implement the session management endpoints — starting a new onboarding session, retrieving session details, and getting checklist progress. These endpoints are what the frontend calls to initialize and track an onboarding run.

### Sub-tasks

#### 13.1 — Start Onboarding Session Endpoint
```python
@router.post("/onboarding/start")
async def start_onboarding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user already has an in_progress session
    # If yes, return that session (idempotent)
    # If no:
    #   - Create new OnboardingSession row with status=in_progress
    #   - Set current_fsm_state=WELCOME
    #   - Return session_id and initial agent greeting
    greeting = "Hi! I'm O.N.E — your Onboarding Navigation Environment. I'm here to guide you through your first days at the company. Let's start with the basics — what's your full name and email address?"
    return {"session_id": str(session.id), "message": greeting}
```

#### 13.2 — Get Session Details Endpoint
```python
@router.get("/onboarding/{session_id}")
async def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Load session, persona, and current FSM state
    # Verify current_user owns this session (or is hr_admin)
    pass
```

#### 13.3 — Get Progress Endpoint
```python
@router.get("/onboarding/{session_id}/progress")
async def get_progress(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist_service = ChecklistService(db)
    progress = await checklist_service.get_progress(session_id)
    return progress
    # Returns: total_items, completed, pending, skipped, percent_complete, current_item, items[]
```

#### 13.4 — Checklist Update Endpoint
```python
@router.patch("/checklist/{item_id}")
async def update_checklist_item(
    item_id: str,
    request: UpdateChecklistRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist_service = ChecklistService(db)
    updated = await checklist_service.update_item_status(
        item_id=item_id, status=request.status, notes=request.notes
    )
    return updated
```

### Acceptance Criteria
- [ ] `POST /onboarding/start` creates a new session and returns session_id with greeting
- [ ] Starting twice returns the existing in-progress session (no duplicates)
- [ ] `GET /onboarding/{id}/progress` returns correct counts
- [ ] `PATCH /checklist/{id}` updates status in DB
- [ ] User cannot access another user's session (403 returned)

---

---

# SPRINT 4 — Chat UI + Checklist (Week 4)

---

## T-14 · React Chat Interface

**Sprint:** 4 — Week 4  
**Estimated Effort:** 8–10 hours  
**Owner:** Frontend team member  
**Dependencies:** T-09, T-13

### Purpose
Build the developer-facing chat UI — the primary interface of the entire product. A good chat interface feels responsive and natural. The developer should feel like they are talking to a knowledgeable colleague, not filling out a form.

### Sub-tasks

#### 14.1 — App Structure and Routing
In `frontend/src/main.jsx`, set up React Router:
```
/login          → LoginPage
/chat           → ChatPage (protected — requires auth)
/dashboard      → AdminDashboardPage (protected — requires hr_admin role)
```

Create `frontend/src/context/AuthContext.jsx` to store JWT token and user info across the app. The token is stored in `sessionStorage` (cleared when browser closes — more secure than localStorage for this use case).

#### 14.2 — Login Page
`frontend/src/pages/LoginPage.jsx`:
- Email and password fields
- Submit calls `POST /api/v1/auth/login`
- On success: store token in AuthContext, redirect to `/chat`
- On failure: show error message "Invalid email or password"
- Simple, clean design — center-aligned card with O.N.E logo/name

#### 14.3 — Main Chat Page Layout
`frontend/src/pages/ChatPage.jsx` — two-panel layout:
```
┌─────────────────────────────────────┬──────────────────────┐
│         CHAT PANEL (70%)            │  CHECKLIST PANEL(30%)│
│                                     │                      │
│  [Message bubbles scroll here]      │  Progress: 58%       │
│                                     │  ████████░░ 7/12     │
│                                     │                      │
│                                     │  ✅ GitHub access    │
│                                     │  ✅ Jira access      │
│                                     │  🔵 Local dev setup  │
│                                     │  ⬜ Read ADRs        │
│                                     │  ⬜ API guidelines   │
│                                     │                      │
│  [Input box + Send button]          │                      │
└─────────────────────────────────────┴──────────────────────┘
```

#### 14.4 — Message Bubble Components
`frontend/src/components/MessageBubble.jsx`:
- **User messages**: right-aligned, blue background (`bg-blue-500 text-white`)
- **Agent messages**: left-aligned, gray background (`bg-gray-100 text-gray-900`), with a small "O.N.E" avatar
- **Typing indicator**: three animated dots, shown while waiting for API response
- Messages render Markdown (use `react-markdown` package for bold, code, lists)
- Install: `npm install react-markdown`

#### 14.5 — Chat Input Component
`frontend/src/components/ChatInput.jsx`:
- Textarea (auto-resizes up to 4 lines)
- Send button (disabled while response loading)
- Press Enter to send, Shift+Enter for newline
- Quick action buttons below input:
  - "Mark as done" → pre-fills "I have completed this task"
  - "Ask for help" → pre-fills "Can you explain this in more detail?"
  - "Skip this" → pre-fills "Can I skip this task?"
- Clear input after send

#### 14.6 — API Integration Layer
Create `frontend/src/api/`:

`auth.js`:
```javascript
export const login = (email, password) =>
  axios.post('/api/v1/auth/login', { email, password });
```

`chat.js`:
```javascript
export const startSession = () =>
  authAxios.post('/api/v1/onboarding/start');

export const sendMessage = (sessionId, message) =>
  authAxios.post(`/api/v1/chat/${sessionId}/message`, { message });

export const getChatHistory = (sessionId) =>
  authAxios.get(`/api/v1/chat/${sessionId}/history`);
```

`checklist.js`:
```javascript
export const getProgress = (sessionId) =>
  authAxios.get(`/api/v1/onboarding/${sessionId}/progress`);
```

Create a shared `authAxios` instance with the JWT token in the Authorization header:
```javascript
const authAxios = axios.create({ baseURL: import.meta.env.VITE_API_URL });
authAxios.interceptors.request.use(config => {
  const token = sessionStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

#### 14.7 — Chat State Management Hook
Create `frontend/src/hooks/useChat.js`:
```javascript
export function useChat(sessionId) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const sendMessage = async (text) => {
    // Optimistically add user message to UI immediately
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setIsLoading(true);
    try {
      const response = await chatApi.sendMessage(sessionId, text);
      setMessages(prev => [...prev, { role: 'assistant', content: response.data.reply }]);
    } finally {
      setIsLoading(false);
    }
  };
  
  return { messages, sendMessage, isLoading };
}
```

### Acceptance Criteria
- [ ] Login page authenticates and stores JWT token
- [ ] Chat page shows two-panel layout on desktop
- [ ] User messages appear right-aligned (blue), agent messages left-aligned (gray)
- [ ] Typing indicator appears while waiting for API response
- [ ] Quick action buttons pre-fill the input correctly
- [ ] Messages render Markdown (bold, code blocks, numbered lists)
- [ ] Enter sends message, Shift+Enter adds newline
- [ ] Auto-scrolls to the latest message

---

## T-15 · Real-Time Checklist Sidebar

**Sprint:** 4 — Week 4  
**Estimated Effort:** 5–6 hours  
**Owner:** Frontend team member  
**Dependencies:** T-08, T-14

### Purpose
The checklist sidebar gives the developer a persistent view of their onboarding progress. It should update in real time as the agent marks items complete during the conversation — the developer should see the checkmark appear without refreshing.

### Sub-tasks

#### 15.1 — Progress Bar Component
`frontend/src/components/ProgressBar.jsx`:
```jsx
// Visual progress bar that fills based on percent_complete
// Shows "7 of 12 tasks complete (58%)"
// Green fill, smooth CSS transition on update
// Uses percent_complete from the /progress API response
```

#### 15.2 — Checklist Item Component
`frontend/src/components/ChecklistItem.jsx`:
```jsx
// Each item shows:
// Status icon: ✅ completed (green), 🔵 in_progress (blue), ⬜ pending (gray), ⏭️ skipped (yellow)
// Item title (bold if current item)
// Category badge (small colored pill: access/tooling/documentation/compliance/team)
// Required badge (red dot if required: true)
// completed_at timestamp (small text) if status=completed
```

#### 15.3 — Checklist Sidebar Component
`frontend/src/components/ChecklistSidebar.jsx`:
```jsx
// Shows ProgressBar at top
// Groups items by category
// Highlights the current in_progress item with a blue left border
// Shows completion count per category: "Documentation (2/4)"
// Scroll independently from chat panel (overflow-y-auto)
```

#### 15.4 — Polling for Progress Updates
```javascript
// Poll GET /onboarding/{session_id}/progress every 3 seconds
// Update checklist sidebar when response changes
// Stop polling when session status = "completed"
useEffect(() => {
  const interval = setInterval(async () => {
    const progress = await checklistApi.getProgress(sessionId);
    setProgress(progress.data);
  }, 3000);
  return () => clearInterval(interval);
}, [sessionId]);
```

Polling every 3 seconds is simple and sufficient — WebSocket streaming is a Semester 2 enhancement.

#### 15.5 — Conversation History on Load
When the `ChatPage` loads:
1. Call `GET /api/v1/onboarding/start` → get session_id (or create new session)
2. Call `GET /api/v1/chat/{session_id}/history` → load existing messages
3. Render all past messages in the chat window
4. Scroll to bottom

This ensures that if a developer closes and reopens the browser, they see their conversation history.

### Acceptance Criteria
- [ ] Progress bar shows correct percentage and animates on update
- [ ] Status icons are correct for all four states (completed, in_progress, pending, skipped)
- [ ] Current item highlighted with visual indicator
- [ ] Items grouped by category with category completion count
- [ ] Checklist updates automatically within 3 seconds of the agent marking an item
- [ ] Past conversation history loads on page refresh

---

## T-16 · Conversation History API

**Sprint:** 4 — Week 4  
**Estimated Effort:** 2–3 hours  
**Owner:** Backend team  
**Dependencies:** T-09, T-13

### Purpose
Implement the endpoint that returns the full conversation history for a session, so the frontend can load past messages when a developer returns to the chat.

### Sub-tasks

#### 16.1 — Conversation History Endpoint
```python
@router.get("/chat/{session_id}/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(ConversationLog)\
        .filter(ConversationLog.session_id == session_id)\
        .filter(ConversationLog.role != "system")\  # don't expose system prompts
        .order_by(ConversationLog.created_at.asc())\
        .all()
    return {"session_id": session_id, "messages": [
        {"role": log.role, "content": log.content, "created_at": log.created_at}
        for log in logs
    ]}
```

#### 16.2 — Message Persistence
Ensure `AgentOrchestrator._persist_state()` saves both user and assistant messages to `conversation_logs` with the correct role field. System prompts should be stored with `role="system"` but NOT returned by the history endpoint.

### Acceptance Criteria
- [ ] History endpoint returns all user and assistant messages in chronological order
- [ ] System messages are not returned to the frontend
- [ ] Frontend loads and displays history on page refresh
- [ ] Messages have timestamps

---

---

# SPRINT 5 — HR Notification + Dashboard (Week 5)

---

## T-17 · Gmail SMTP Email Service

**Sprint:** 5 — Week 5  
**Estimated Effort:** 4–5 hours  
**Owner:** Backend team  
**Dependencies:** T-08, T-09

### Purpose
Implement the HR notification email that is sent when a developer completes all required onboarding tasks. This is the final output of the onboarding process — a structured report that HR and the engineering manager can review.

### Sub-tasks

#### 17.1 — Gmail App Password Setup
Document these steps in `docs/gmail-smtp-setup.md`:
1. Go to `myaccount.google.com`
2. Security → 2-Step Verification → enable it
3. Security → App passwords → create one called "ONE Onboarding Agent"
4. Copy the 16-character app password
5. Set `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` in `.env`

#### 17.2 — Implement Email Service
Create `backend/app/services/email_service.py`:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self):
        self.gmail_address = os.getenv("GMAIL_ADDRESS")
        self.gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.hr_email = os.getenv("HR_EMAIL")

    def send_email(self, to: str, subject: str, html_body: str, cc: list = None) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.gmail_address
            msg["To"] = to
            if cc:
                msg["Cc"] = ", ".join(cc)
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_address, self.gmail_app_password)
                recipients = [to] + (cc or [])
                server.sendmail(self.gmail_address, recipients, msg.as_string())
            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
```

#### 17.3 — Build HTML Email Template
Create `backend/app/services/email_template.py`:

The `generate_completion_email_html()` function produces an HTML email with:
- Header: "✅ Onboarding Completed — [Name] ([Role])"
- Employee details table: name, email, role, team, tech stack, start date
- Completed items section: numbered list with green checkmarks
- Pending/Skipped items section (if any): with yellow warning icons
- Completion details: timestamp, total duration in hours/days, session ID
- Confidence score: percentage based on completed/required items
- Footer: "This is an automated notification from O.N.E"

The email must be well-formatted plain HTML (no external CSS frameworks — email clients don't support them). Use inline styles only.

#### 17.4 — Implement HR Notification Service
Create `backend/app/services/hr_notification_service.py`:

```python
class HRNotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()

    async def send_completion_email(self, session_id: str) -> bool:
        # 1. Load session and persona from DB
        # 2. Load all checklist items for this session
        # 3. Split into completed and pending lists
        # 4. Calculate confidence score: completed_required / total_required * 100
        # 5. Calculate duration: session.completed_at - session.started_at
        # 6. Generate HTML email
        # 7. Send to HR email, CC developer email
        # 8. Update session: hr_notified=True, hr_notification_sent_at=now, status=completed
        pass

    def calculate_confidence(self, checklist: list) -> int:
        required = [i for i in checklist if i.required]
        completed_required = [i for i in required if i.status == "completed"]
        if not required:
            return 100
        return round(len(completed_required) / len(required) * 100)
```

#### 17.5 — Connect to Agent send_hr_completion_email Tool
In `AgentOrchestrator._execute_tool()`, when tool name is `send_hr_completion_email`:
```python
hr_service = HRNotificationService(self.db)
success = await hr_service.send_completion_email(self.session_id)
if success:
    return {"status": "success", "message": "HR completion email sent successfully"}
else:
    return {"status": "error", "message": "Failed to send email — please check logs"}
```

### Acceptance Criteria
- [ ] `send_email()` successfully sends to a real Gmail address (manual test)
- [ ] HTML email renders correctly in Gmail (desktop and mobile)
- [ ] Email includes all sections: employee details, completed items, pending items, confidence score
- [ ] Session is marked `hr_notified=True` after successful send
- [ ] Email is CC'd to the developer's email
- [ ] Agent triggers email correctly when tool call is executed

---

## T-18 · Admin APIs for HR Dashboard

**Sprint:** 5 — Week 5  
**Estimated Effort:** 4–5 hours  
**Owner:** Backend team  
**Dependencies:** T-02, T-12, T-13

### Purpose
Implement the backend APIs that power the HR admin dashboard — session listing, metrics, and the ability to manually resend HR notification emails.

### Sub-tasks

#### 18.1 — Sessions List Endpoint (Paginated)
```python
@router.get("/admin/sessions")
async def list_sessions(
    page: int = 1,
    page_size: int = 20,
    role: str = None,       # filter by developer role
    status: str = None,     # filter by session status (in_progress/completed)
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hr_admin_user)
):
    # Query onboarding_sessions joined with users
    # Apply optional filters
    # Return paginated list with: session_id, employee name, role, status, 
    #   started_at, completed_at, percent_complete
    pass
```

#### 18.2 — Metrics Endpoint
```python
@router.get("/admin/metrics")
async def get_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hr_admin_user)
):
    # Calculate:
    # - total_sessions (all time)
    # - active_sessions (status=in_progress)
    # - completed_sessions (status=completed)
    # - completion_rate: completed/total * 100
    # - avg_duration_hours: average of (completed_at - started_at) for completed sessions
    # - completions_this_week: completed in last 7 days
    # Return as dict
    pass
```

#### 18.3 — Resend HR Email Endpoint
```python
@router.post("/admin/notify-hr/{session_id}")
async def resend_hr_notification(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hr_admin_user)
):
    hr_service = HRNotificationService(db)
    success = await hr_service.send_completion_email(session_id)
    return {"success": success}
```

### Acceptance Criteria
- [ ] Sessions list returns paginated results with correct fields
- [ ] Role and status filters work correctly
- [ ] Metrics endpoint returns accurate counts and averages
- [ ] Resend endpoint triggers a new email

---

## T-19 · HR Admin Dashboard Frontend

**Sprint:** 5 — Week 5  
**Estimated Effort:** 6–7 hours  
**Owner:** Frontend team member  
**Dependencies:** T-14, T-18

### Purpose
Build the HR-facing admin dashboard that shows all onboarding sessions, metrics, and per-developer progress. HR staff should be able to see at a glance who has completed onboarding and who is still in progress.

### Sub-tasks

#### 19.1 — Dashboard Layout
`frontend/src/pages/AdminDashboardPage.jsx`:
- Top row: 4 metric cards (Total Sessions, Active, Completed, Avg Duration)
- Middle: Sessions table with filter controls
- Bottom: (Semester 2 — analytics charts)

#### 19.2 — Metric Cards Component
`frontend/src/components/MetricCard.jsx`:
```jsx
// Props: title, value, subtitle, color
// Example: title="Completion Rate", value="72%", subtitle="of all sessions", color="green"
// Simple white card with number, label, colored left border
```

#### 19.3 — Sessions Table
`frontend/src/components/SessionsTable.jsx`:
```
| Employee | Role | Status | Started | Progress | Actions |
|----------|------|--------|---------|----------|---------|
| Jane Doe | Backend (Senior) | ✅ Completed | Mar 1 | 12/12 | View |
| Alex Kim | Frontend (Junior) | 🔵 In Progress | Mar 3 | 7/12 (58%) | View | Resend Email |
```
- Click "View" → go to `/dashboard/sessions/{session_id}` for per-developer detail
- "Resend Email" button only shown for completed sessions

#### 19.4 — Per-Developer Session Detail Page
`frontend/src/pages/SessionDetailPage.jsx`:
- Shows employee info (name, email, role, tech stack)
- Shows full checklist with status of every item
- Shows conversation log (read-only)
- "Resend HR Email" button

#### 19.5 — Role-Based Route Protection
Only `hr_admin` role can access `/dashboard`. Add a `ProtectedRoute` component:
```jsx
function ProtectedRoute({ requiredRole, children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (requiredRole && user.role !== requiredRole) return <Navigate to="/chat" />;
  return children;
}
```

### Acceptance Criteria
- [ ] Dashboard accessible only to hr_admin role
- [ ] Metric cards show correct values from /admin/metrics
- [ ] Sessions table shows all sessions with correct status and progress
- [ ] Role and status filters work
- [ ] Per-session detail page shows checklist breakdown
- [ ] Resend email button works and shows success/failure feedback

---

---

# SPRINT 6 — Testing, Polish, Demo Prep (Week 6)

---

## T-20 · End-to-End Testing

**Sprint:** 6 — Week 6  
**Estimated Effort:** 6–8 hours  
**Owner:** All team members  
**Dependencies:** All previous tasks

### Purpose
Verify the complete onboarding flow works end-to-end — from developer login through to HR email delivery. Find and fix integration bugs before the demo.

### Sub-tasks

#### 20.1 — Manual E2E Test Script
Document a complete manual test walkthrough in `docs/e2e-test-script.md`:

**Test Case 1: Happy Path — Senior Backend Python Developer**
1. Open `localhost:5173` → login as `dev@company.com`
2. Session starts, agent says hello
3. Type: "Hi, I'm Rahul Sharma, rahul@test.com"
4. Verify: agent extracts name and email
5. Type: "I'm a senior backend developer"
6. Verify: role=backend extracted
7. Type: "I mostly work with Python and FastAPI"
8. Verify: checklist generated (should see 10-12 items in sidebar)
9. Type: "What do I need to do for GitHub access?"
10. Verify: agent retrieves from knowledge base and cites source
11. Type: "I've set up GitHub access"
12. Verify: agent marks item complete in sidebar (within 3 seconds)
13. Continue through at least 3 more items
14. Verify progress bar updates correctly
15. Complete all required items
16. Type: "I've finished everything"
17. Verify: agent offers to send HR email
18. Type: "Yes, please send it"
19. Verify: HR email received in Gmail

**Test Case 2: Intern Frontend Developer**
- Verify different checklist items (git workflow tutorial, no ADR review)
- Verify more hand-holding in agent responses

**Test Case 3: HR Admin Dashboard**
- Login as `hr@company.com`
- Verify both test sessions appear in dashboard
- Verify metrics are correct
- Verify "View" opens session detail with correct checklist

#### 20.2 — pytest Unit Tests
Ensure the following are tested:
- `test_persona_agent.py` — 5 extraction test cases
- `test_checklist_service.py` — filtering for 4 persona combinations
- `test_rag_service.py` — 5 retrieval test cases
- `test_auth.py` — login, invalid password, JWT validation
- `test_email_service.py` — email formatting (mock SMTP call)

Run: `cd backend && pytest tests/ -v`

#### 20.3 — LLM Golden Test Cases
Create `backend/tests/test_golden_cases.py`:
```python
golden_test_cases = [
    {
        "test_id": "GT-001",
        "description": "Agent cites source for Python version question",
        "input": "What version of Python do we use?",
        "expected_in_response": "3.11",
        "expected_source_cited": True
    },
    {
        "test_id": "GT-002",
        "description": "Agent calls mark_checklist_item on task completion",
        "input": "I've finished setting up my local environment",
        "expected_tool_called": "mark_checklist_item"
    },
    {
        "test_id": "GT-003",
        "description": "Agent gracefully redirects off-topic question",
        "input": "What is the best restaurant near the office?",
        "expected_not_in_response": ["restaurant", "food", "I recommend"],
        "expected_redirect": True
    },
    {
        "test_id": "GT-004",
        "description": "Agent does not skip compliance task when asked",
        "input": "Can I skip the NDA signing?",
        "expected_behavior": "agent_blocks_skip_of_required_item"
    },
    {
        "test_id": "GT-005",
        "description": "Agent offers HR email when all items done",
        "setup": "mark all required checklist items as completed",
        "input": "I've finished everything",
        "expected_tool_called": "get_checklist_status"
    }
]
```

Run each case and log pass/fail results.

### Acceptance Criteria
- [ ] E2E happy path test completes without errors
- [ ] HR email received at destination Gmail address
- [ ] All pytest unit tests pass (`pytest tests/ -v` shows 0 failures)
- [ ] At least 4 of 5 golden test cases pass
- [ ] RAG correctly returns the expected document for all 5 retrieval queries

---

## T-21 · Bug Fixes, Code Cleanup, and Documentation

**Sprint:** 6 — Week 6  
**Estimated Effort:** 4–5 hours  
**Owner:** All team members  
**Dependencies:** T-20

### Purpose
Fix all bugs found during E2E testing, clean up the codebase for the demo and final submission, and ensure documentation is complete.

### Sub-tasks

#### 21.1 — Bug Fix Priority List
After T-20 testing, create a prioritized bug list. Address all P0 (blocks demo) and P1 (demo degraded) bugs before the demo.

#### 21.2 — Code Cleanup Checklist
- Remove all `print()` debug statements (replace with `logging.info()`)
- Remove all `TODO` comments that were not addressed
- Ensure all `.env` values are loaded from environment (no hardcoded values)
- Add docstrings to all public functions in `agents/` and `services/`
- Ensure all API routes have response_model defined
- Run Black formatter: `black backend/app/`
- Fix any ESLint warnings in frontend: `cd frontend && npm run lint`

#### 21.3 — README Update
Update `README.md` with:
- Project description (2-3 sentences)
- Architecture diagram image
- Prerequisites (Python 3.11+, Node 18+, PostgreSQL 15+)
- Step-by-step setup instructions (clone, `.env`, db migration, seed, ingest, run)
- How to run tests
- Team members and guide

#### 21.4 — API Documentation
FastAPI auto-generates documentation at `http://localhost:8000/docs`. Verify:
- All endpoints appear
- All request/response schemas are documented
- Example values are included in Pydantic models

### Acceptance Criteria
- [ ] Zero `print()` debug statements in production code
- [ ] No hardcoded API keys or passwords in any source file
- [ ] `black` and `eslint` report no errors
- [ ] README setup instructions work for a fresh clone
- [ ] FastAPI `/docs` shows all 13 endpoints

---

## T-22 · Demo Preparation and Final Submission

**Sprint:** 6 — Week 6  
**Estimated Effort:** 3–4 hours  
**Owner:** All team members  
**Dependencies:** T-20, T-21

### Purpose
Prepare a polished, reliable demo environment and all final submission deliverables.

### Sub-tasks

#### 22.1 — Demo Environment Setup
- Create a `demo_seed.py` script that:
  - Clears all test data from the database
  - Creates 2 fresh test users (1 employee, 1 HR admin)
  - Re-runs the ChromaDB ingestion
  - Prints login credentials for the demo
- Test running this script 3 times to ensure it is idempotent

#### 22.2 — Demo Script
Write `docs/demo-script.md` — a step-by-step walkthrough of what to show:
1. Show the login page (explain: React + Vite frontend)
2. Login as developer → start chat (explain: FastAPI backend, JWT auth)
3. Type responses for profiling (explain: Gemini extraction of persona)
4. Show checklist appearing in sidebar (explain: personalised checklist from DB template)
5. Ask a question about Python setup (explain: RAG retrieves from ChromaDB, cites source)
6. Complete 3-4 tasks (explain: agent tool calls mark items in PostgreSQL)
7. Show progress bar updating (explain: frontend polls /progress API)
8. Complete all required tasks → trigger HR email (explain: Gmail SMTP, smtplib)
9. Switch to HR admin login → show dashboard (explain: role-based access, session metrics)
10. Show the received email in Gmail

#### 22.3 — Final Deliverables Checklist
For project submission, ensure you have:
- [ ] GitHub repo link (complete code, all branches)
- [ ] Technical plan document (the full `.docx` from the previous task)
- [ ] This `tasks.md` file
- [ ] `README.md` with setup instructions
- [ ] Architecture diagrams in `docs/architecture/`
- [ ] API contract documentation
- [ ] Working demo (recorded video as backup if live demo has issues)
- [ ] Presentation slides (Semester 1 deliverables summary)

#### 22.4 — Backup Demo Video
Record a 5-7 minute screen recording of the complete happy-path demo. This is your fallback if the live demo environment has issues. Upload to Google Drive and add the link to the README.

### Acceptance Criteria
- [ ] `demo_seed.py` runs cleanly and sets up a fresh demo state
- [ ] Demo script has been rehearsed at least twice end-to-end
- [ ] Demo video recorded and accessible
- [ ] All final submission deliverables collected and ready
- [ ] Both team members who will present know the talking points for each demo step

---

## Summary Table

| Task | Sprint | Description | Effort |
|------|--------|-------------|--------|
| T-01 | 1 | Project scaffolding and repository setup | 4-5 hrs |
| T-02 | 1 | PostgreSQL schema design and setup | 5-6 hrs |
| T-03 | 1 | Knowledge base creation (markdown docs) | 6-8 hrs |
| T-04 | 1 | Architecture diagrams and API contract | 3-4 hrs |
| T-05 | 2 | Gemini API integration and LLM client | 4-5 hrs |
| T-06 | 2 | FSM implementation | 4-5 hrs |
| T-07 | 2 | Persona detection agent | 5-6 hrs |
| T-08 | 2 | Dynamic checklist generator | 5-6 hrs |
| T-09 | 2 | Core agent orchestrator and message handler | 6-7 hrs |
| T-10 | 3 | ChromaDB setup and ingestion pipeline | 5-6 hrs |
| T-11 | 3 | RAG retrieval service | 5-6 hrs |
| T-12 | 3 | JWT authentication system | 4-5 hrs |
| T-13 | 3 | Onboarding session management API | 4-5 hrs |
| T-14 | 4 | React chat interface | 8-10 hrs |
| T-15 | 4 | Real-time checklist sidebar | 5-6 hrs |
| T-16 | 4 | Conversation history API | 2-3 hrs |
| T-17 | 5 | Gmail SMTP email service | 4-5 hrs |
| T-18 | 5 | Admin APIs for HR dashboard | 4-5 hrs |
| T-19 | 5 | HR admin dashboard frontend | 6-7 hrs |
| T-20 | 6 | End-to-end testing | 6-8 hrs |
| T-21 | 6 | Bug fixes, cleanup, documentation | 4-5 hrs |
| T-22 | 6 | Demo preparation and final submission | 3-4 hrs |
| | | **Total estimated effort** | **~113-131 hrs** |

---

## Dependency Graph

```
T-01 (Scaffold)
  ├── T-02 (Database)
  │     ├── T-08 (Checklist Generator)
  │     │     └── T-09 (Orchestrator)
  │     ├── T-12 (Auth)
  │     │     └── T-13 (Session API) → T-15, T-16
  │     └── T-04 (Architecture)
  ├── T-03 (Knowledge Base)
  │     └── T-10 (ChromaDB Ingestion)
  │           └── T-11 (RAG Service)
  │                 └── T-09 (Orchestrator)
  └── T-05 (Gemini Client)
        ├── T-06 (FSM)
        │     └── T-07 (Persona Agent) → T-09
        └── T-09 (Orchestrator)

T-09 (Orchestrator) → T-14 (Chat UI) → T-15 (Sidebar) → T-19 (HR Dashboard)
T-17 (Email) → T-09
T-18 (Admin APIs) → T-19 (HR Dashboard)
T-19 → T-20 (E2E Testing) → T-21 (Cleanup) → T-22 (Demo)
```

---

*Document maintained by Group 28 — O.N.E Project Team*  
*Vivekanand Education Society's Institute of Technology, Department of Information Technology*