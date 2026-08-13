# O.N.E. (Onboarding Navigation Environment) - LangGraph & Agentic UX Roadmap

**Project Scope:** Refactor the O.N.E. architecture to utilize a LangGraph State Machine, implement Hybrid Search, establish a dynamic role-based task checklist, and build a conversational state flow for 0% progress new hires. 
**Target Model:** Local Qwen 2.5 (3B) via Ollama. 

---

## Task 1: Database Schema Expansion & Targeted Seeding
**Objective:** Update the Supabase database to support role-based tracking and seed the specific dummy users for the academic demonstration.
*   **Action 1.1:** Extend the `users` (or `onboarding_sessions`) table to include `department_role` (Enum: `frontend dev`, `backend dev`, `AI dev`, `cloud`, `IT`, `database dev`).
*   **Action 1.2:** Add a `tasks_completed` integer column and an `onboarding_progress` percentage column.
*   **Action 1.3:** Create a script (`seed_demo_users.py`) that uses MCP to wipe all current users **EXCEPT** the Master Admin.
*   **Action 1.4:** Seed the following strictly defined users (Password for all: `123456`):
    *   `archit123@gmail.com` (Archit Chitte) | Role: frontend dev | Tasks Done: 6
    *   `parth123@gmail.com` (Parth Narkar) | Role: database dev | Tasks Done: 15
    *   `manas123@gmail.com` (Manas Patil) | Role: backend dev | Tasks Done: 10
    *   `harsh123@gmail.com` (Harsh Patil) | Role: AI dev | Tasks Done: 0 (Triggers Onboarding Flow)

## Task 2: Role-Specific Tasklist Generation & Database Mapping
**Objective:** Generate the standard operating procedure (SOP) tasks for the 6 fixed roles and store them relationally.
*   **Action 2.1:** Create a JSON or Python dictionary defining ~20 sequential tasks for each of the 6 roles (e.g., Frontend: "Install Node", "Clone Repo", "Run Storybook").
*   **Action 2.2:** Create a `role_tasks` table in Supabase to store these arrays.
*   **Action 2.3:** Map the user's `tasks_completed` integer to this array (e.g., if Manas has 10 tasks done, his "next task" is index 10 in the backend dev array).
*   **Action 2.4:** Export these task lists as Markdown files and ingest them into the corporate Knowledge Base so the RAG agent is aware of them.

## Task 3: Hybrid Search Implementation (ChromaDB + BM25)
**Objective:** Build the dual-engine retrieval system for exact code snippet matching and semantic understanding.
*   **Action 3.1:** Initialize `Chroma` (Dense Vector Search) using local HuggingFace embeddings (`all-MiniLM-L6-v2`).
*   **Action 3.2:** Initialize `BM25Retriever` (Sparse Keyword Search) on the `knowledge_base` markdown directory.
*   **Action 3.3:** Combine them using LangChain's `EnsembleRetriever` with a 50/50 weight distribution.
*   **Action 3.4:** Wrap this Hybrid Retriever into a `@tool` named `search_corporate_knowledge`.

## Task 4: LangGraph State Machine & Supervisor Setup
**Objective:** Replace the basic LangChain agent with a deterministic LangGraph StateGraph.
*   **Action 4.1:** Define the `AgentState` TypedDict containing: `messages` (chat history), `user_id`, `user_role`, `progress`, and `current_task`.
*   **Action 4.2:** Build the routing nodes:
    *   `OnboardingNode`: Handles the 3-question loop for 0% users.
    *   `TaskNode`: Handles requests like "What is my next task?" or "I finished this."
    *   `RAGNode`: Executes the Hybrid Search for company questions.
*   **Action 4.3:** Create conditional edges (Router) so the LLM decides which node to activate based on the user's prompt.

## Task 5: Conversational RAG (Memory Injection)
**Objective:** Ensure the LangGraph agent remembers context seamlessly via Supabase.
*   **Action 5.1:** Update the `POST /api/v1/chat` endpoint to fetch the last 10 messages from the `conversation_logs` table before invoking the graph.
*   **Action 5.2:** Inject these messages into the `AgentState` so Qwen 3B has immediate conversational context (e.g., remembering what port Postgres runs on).
*   **Action 5.3:** Ensure the system prompt dynamically injects the user's name, role, and current progress percentage on every turn.

## Task 6: Initial 0% Onboarding Flow (The 3-Question Gate)
**Objective:** Build the strict introductory conversation for new hires (Harsh Patil's flow).
*   **Action 6.1:** Add logic in the FastAPI router: If a user logs in and their progress is `0` and role is `null`, force the `OnboardingNode` in LangGraph.
*   **Action 6.2:** Systematically prompt: "Hi! I'm O.N.E... what's your full name?" -> Wait for reply.
*   **Action 6.3:** Prompt: "What is your email id?" -> Wait for reply.
*   **Action 6.4:** Prompt: "What is your position? (frontend dev, backend dev, AI dev, cloud, IT, database dev)" -> Wait for reply.
*   **Action 6.5:** Upon completing the form, update the Supabase user record with this data, generate their checklist, and transition them out of the 0% state.

## Task 7: AI Task Management Tools (NLP Triggers)
**Objective:** Give the LLM the ability to read and mutate the user's task state in the database.
*   **Action 7.1:** Create a `@tool` called `get_current_task(user_id)`. When the user asks "What should I do next?", the LLM calls this to fetch task `N+1`.
*   **Action 7.2:** Create a `@tool` called `mark_task_complete(user_id)`. When the user says "I finished it" or "Task done", the LLM executes this tool to increment `tasks_completed` by +1 in Supabase.

## Task 8: UI Reintegration - Checklist Page & Actions
**Objective:** Build clean, functional UI elements for task tracking without cluttering the chat.
*   **Action 8.1:** Create a new React route/component: `/checklist`.
*   **Action 8.2:** Fetch the user's specific ~20 task array from the backend and render it as a clean list (completed tasks crossed out, current task highlighted).
*   **Action 8.3:** Add a functional "Mark as Done" button next to the active task.
*   **Action 8.4:** Wire this button to a new FastAPI endpoint (`POST /api/v1/tasks/complete`) which increments the database counter (mirroring the NLP tool from Task 7).

## Task 9: Authentication & JWT Pipeline Validation
**Objective:** Ensure secure routing based on database state.
*   **Action 9.1:** Verify the login endpoint returns a valid JWT containing the user's `email` and `role`.
*   **Action 9.2:** On the React frontend, ensure routing strictly directs users to `/chat` upon login, and the UI adapts based on whether the DB returns a 0% progress flag vs an active progress flag.
*   **Action 9.3:** Verify Admin transcripts correctly capture and differentiate chats from all four dummy users securely.

## Task 10: End-to-End Testing & VRAM Context Optimization
**Objective:** QA the entire pipeline strictly against the hardware limits (Qwen 3B, 6GB VRAM).
*   **Action 10.1:** Execute E2E login flow with `harsh123@gmail.com` to verify the 3-question sequence triggers perfectly.
*   **Action 10.2:** Execute E2E login with `manas123@gmail.com` (10 tasks done) and ask "What is my next task?". Verify it fetches Task 11.
*   **Action 10.3:** Test Context Window: Ensure the system prompt + chat history + retrieved RAG documents do not exceed ~4,000 tokens to keep Qwen 3B generating fast on the RTX 4050.
*   **Action 10.4:** Fix any Pydantic parsing errors where the smaller 3B model might format tool-calls slightly incorrectly.