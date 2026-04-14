# O.N.E. (Onboarding Navigation Environment)

O.N.E. is a premium, AI-powered onboarding assistant designed to streamline the developer experience within technical organizations. By combining **Gemini 2.0 Flash**, **ChromaDB (RAG)**, and a **Finite State Machine (FSM)** orchestrator, O.N.E. provides a tailored, interactive onboarding journey for engineers.

![O.N.E. HR Dashboard](https://img.shields.io/badge/Design-Warm_Editorial_Minimalism-F7F5F0)
![Backend](https://img.shields.io/badge/Stack-FastAPI_|_PostgreSQL-005571)
![AI](https://img.shields.io/badge/AI-Gemini_2.0_|_ChromaDB-blue)

## 🏗️ Architecture

O.N.E. is built with a decoupled architecture focused on scalability and "Warm Editorial Minimalism" design principles.

### Backend (Python/FastAPI)
- **Agent Orchestrator**: The central brain managing multi-turn conversations, tool calling, and state transitions.
- **FSM Controller**: Manages the onboarding lifecycle stages (`WELCOME` → `PROFILING` → `PLAN_GENERATION` → `EXECUTION` → `REVIEW` → `COMPLETED`).
- **RAG Pipeline**: Semantic search over internal documentation using ChromaDB and Google Gemini Embeddings.
- **Notification Service**: Automated triggers for HR upon completion via Gmail SMTP.
- **Relational Storage**: PostgreSQL (compatible with Neon) for session persistence, conversation logs, and checklists.

### Frontend (React/Tailwind)
- **HR Dashboard**: Real-time metrics and session monitoring for administrators.
- **Developer Chat**: A clean, distraction-free interface for engineers to interact with the assistant.
- **Responsive Layouts**: Optimized for seamless onboarding across devices.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Gemini API Key
- PostgreSQL Database (Neon.tech recommended)
- Gmail App Password (for notifications)

### Backend Setup
1. Navigate to the `backend/` directory.
2. Create a `.env` file based on `.env.example`:
   ```env
   DATABASE_URL=postgresql://...
   GEMINI_API_KEY=your_key_here
   GMAIL_ADDRESS=your_email@gmail.com
   GMAIL_APP_PASSWORD=abcdefg12345
   HR_EMAIL=hr_team@company.com
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   ```
3. Initialize the environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
4. Ingest the Knowledge Base:
   ```bash
   python -m app.core.ingest_knowledge_base
   ```
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 🧪 Testing

O.N.E. includes a comprehensive testing suite to ensure reliability during critical onboarding flows.

- **Unit Tests**: `pytest backend/tests/` (Covers Auth, RAG, Checklist, and FSM)
- **Golden Tests**: `python -m backend.tests.test_golden_cases` (Verifies AI output behavior and tool calling accuracy)
- **Manual E2E**: Detailed walkthrough available in `docs/e2e-test-script.md`

## 🎨 Design Philosophy: Warm Editorial Minimalism
O.N.E. eschews the generic "SaaS Blue" aesthetic for a premium, architectural look:
- **Palette**: Off-white backgrounds (`#F7F5F0`), stark charcoal text (`#1A1A1A`), and subtle border treatments.
- **Typography**: Focused on readability with Inter and mono-space accents.
- **Interaction**: Micro-animations and sharp edges convey a feeling of high-quality craftsmanship.

## 🛠️ Key Utilities
- **RAG Ingestion**: Recursive Markdown chunking for high-fidelity retrieval.
- **Tool Calling**: Native integration for ticking off checklist items and searching knowledge.
- **Admin RBAC**: Secure `hr_admin` routes protecting sensitive metrics and employee data.

---
*Built with ❤️ by the Advanced Agentic Coding Team.*
