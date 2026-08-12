# FastAPI Backend Directory Structure

## Layout
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app init, middleware, router mounts
│   ├── api/
│   │   ├── auth.py          # POST /auth/login, /auth/register
│   │   ├── chat.py          # POST /chat/{session_id}/message
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
*Backend Lead: Archit Verma*
