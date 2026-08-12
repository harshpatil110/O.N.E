# Local Development Environment Setup

## System Requirements
* **OS:** macOS 13+, Ubuntu 22.04+, or Windows 11 with WSL2.
* **RAM:** Minimum 16 GB (32 GB recommended for Ollama models).
* **Storage:** 50 GB free SSD space.

## Backend Setup (Python / FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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
Contact Harshvardhan Patil for credentials.

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
# Expected: {"status": "ok", "service": "O.N.E Backend"}

# Frontend
# Open http://localhost:5173 in your browser
```

---
*Engineering Onboarding — Nexus AI Innovations*
