# Hermes Agent — Supervisor Router Architecture

## Overview
The **Hermes Agent** acts as the central supervisor in Nexus AI Innovations's
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
*Architect: Harshvardhan Patil*
