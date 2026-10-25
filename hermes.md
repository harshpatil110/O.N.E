
# SYSTEM DIRECTIVE: OVERRIDE PLAN MODE -> INITIATE CODE MODE

**CRITICAL INSTRUCTION:** Do not outline an implementation plan. Do not ask for permission to execute. Immediately enter CODE/ACTION mode.

**Project Context:**
O.N.E. (Onboarding Navigation Environment). We have a local instance of Nous Research's **Hermes Agent** running on `http://localhost:8642/v1` with active MCP integrations and connectors for Slack, Notion, Vercel, Jira, and Confluence.

**Current Task:** Integrate Hermes Agent as a Multi-App Execution Sub-Agent inside LangGraph.
**Objective:**

1. Add configuration variables for the Hermes API server (`HERMES_API_URL` and `HERMES_API_KEY`).
2. Create a new LangGraph tool (`delegate_to_hermes`) that forwards queries regarding third-party workspace apps (Slack, Notion, Vercel, Jira, Confluence) to the Hermes Agent API (`POST /v1/chat/completions`) and returns the synthesized output.
3. Bind this tool to the LangGraph supervisor/agent node and update the system prompt so the chatbot seamlessly routes external app requests to Hermes while keeping internal onboarding task queries grounded in PostgreSQL.
4. Add a subtle minimalist badge in the Chat UI when a response uses external workspace context.

### 1. Environment & Config (`backend/.env` & `backend/app/core/config.py` or equivalent)

Add default fallbacks for the Hermes Agent local server:

* `HERMES_API_URL = os.getenv("HERMES_API_URL", "http://localhost:8642/v1/chat/completions")`
* `HERMES_API_KEY = os.getenv("HERMES_API_KEY", "hermes-local-key")`

### 2. Create the Hermes Delegation Tool (`backend/app/core/hermes_tool.py` or inside `task_tools.py`)

Create a robust tool using `httpx` or `requests` that communicates with the Hermes OpenAI-compatible endpoint.

*AI INSTRUCTION: Implement the following tool and bind it to the existing tool list used by the LangGraph agent.*

```python
import os
import requests
from langchain_core.tools import tool

HERMES_API_URL = os.getenv("HERMES_API_URL", "http://localhost:8642/v1/chat/completions")
HERMES_API_KEY = os.getenv("HERMES_API_KEY", "your-secret-key-here")

@tool("delegate_to_hermes")
def delegate_to_hermes(query: str) -> str:
    """
    Use this tool ALWAYS when the developer asks to read, search, or perform actions in connected external workspace apps:
    Slack (messages/channels), Notion (pages/databases), Vercel (deployments/logs), Jira (tickets/sprints/issues), or Confluence (docs/wikis).
    Pass the user's exact request as the 'query'.
    """
    print(f"\n--- ⚡ ROUTING TO HERMES AGENT (MCP GATEWAY) ---")
    print(f"Query: {query}")
  
    headers = {
        "Authorization": f"Bearer {HERMES_API_KEY}",
        "Content-Type": "application/json"
    }
  
    payload = {
        "model": "hermes-agent",
        "messages": [
            {
                "role": "system",
                "content": "You are the Hermes background execution engine for the O.N.E. Developer Onboarding Platform. Execute the requested lookup or action across your connected MCP tools (Slack, Notion, Vercel, Jira, Confluence) and return a clear, concise, factual response."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False
    }
  
    try:
        # Timeout set to 45s to allow Hermes time to execute multi-step MCP tool calls
        response = requests.post(HERMES_API_URL, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        data = response.json()
      
        hermes_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"✅ HERMES RESPONSE RECEIVED ({len(hermes_reply)} chars)")
        return hermes_reply if hermes_reply else "Hermes executed the command but returned an empty response."
      
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to Hermes Agent on port 8642.")
        return "System Error: Unable to reach the local Hermes Agent gateway on port 8642. Ensure `hermes gateway start` is running."
    except Exception as e:
        print(f"❌ HERMES TOOL ERROR: {e}")
        return f"Error communicating with Hermes Agent: {str(e)}"
3. Bind Tool & Update LangGraph Supervisor Prompt (backend/app/core/langgraph_agent.py)
Ensure the LangGraph agent knows when to use internal PostgreSQL tools vs. when to call delegate_to_hermes.

AI INSTRUCTION: 1. Add delegate_to_hermes to the tools = [...] list bound to the LLM (llm.bind_tools(tools)). 2. Update the core system prompt in the agent node so it explicitly knows it has access to Slack, Notion, Vercel, Jira, and Confluence via delegate_to_hermes.

Add this rule to the System Prompt:

Plaintext
EXTERNAL WORKSPACE INTEGRATIONS (HERMES BRIDGE):
If the user asks about Slack messages, Notion documentation, Vercel deployment status, Jira tickets/assigned issues, or Confluence pages, YOU MUST invoke the `delegate_to_hermes` tool with their query and present the returned information clearly. Do not hallucinate external ticket statuses or deployment logs.
4. Verification Checkpoints
[ ] Tool Binding: Is delegate_to_hermes registered in Both the LLM .bind_tools() call and the LangGraph ToolNode?

[ ] Preservation: Does the JIT current_active_task database injection from PostgreSQL remain completely intact?

[ ] Error Handling: If port 8642 is unreachable, does the tool gracefully return a clear message without crashing the FastAPI worker?

Final Output: Output the code added for delegate_to_hermes, the updated tool registration list in the LangGraph setup, and the updated System Prompt.
```
