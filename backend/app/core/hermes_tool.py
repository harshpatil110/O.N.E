import os
import re
import time
import requests
from langchain_core.tools import tool

HERMES_API_URL = os.getenv("HERMES_API_URL", "http://localhost:8642/v1/chat/completions")
HERMES_API_KEY = os.getenv("HERMES_API_KEY", "hermes-local-key")
HERMES_MAX_TOKENS = int(os.getenv("HERMES_MAX_TOKENS", "4096"))

def _log(msg: str) -> None:
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))

def format_hermes_markdown(text: str) -> str:
    """Clean up Hermes output so collapsed single-line tables and headers render cleanly."""
    if not text:
        return text
    # Strip any <think>...</think> blocks if present
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    # Fix collapsed single-line markdown tables: replace "| |" with "|\n|"
    text = re.sub(r'\|\s*\|', '|\n|', text)
    # Ensure headers and bold section titles have a blank line before them
    text = re.sub(r'([^\n])\n(\*\*[A-Z][^*]+\*\*)', r'\1\n\n\2', text)
    return text.strip()

@tool("delegate_to_hermes")
def delegate_to_hermes(query: str) -> str:
    """
    Use this tool ALWAYS when the developer asks to read, search, or perform actions in connected external workspace apps:
    Slack (messages/channels), Notion (pages/databases), Vercel (deployments/logs), Jira (tickets/sprints/issues), or Confluence (docs/wikis).
    Pass the user's exact request as the 'query'.
    """
    _log(f"\n--- [HERMES] ROUTING TO HERMES AGENT (MCP GATEWAY) ---")
    _log(f"Query: {query}")
    start_ts = time.time()

    headers = {
        "Authorization": f"Bearer {HERMES_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "hermes-agent",
        "max_tokens": HERMES_MAX_TOKENS,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are the Hermes background execution engine for the O.N.E. Developer Onboarding Platform. "
                    "Execute the requested lookup or action across your connected MCP tools (Slack, Notion, Vercel, Jira, Confluence).\n\n"
                    "CRITICAL EXECUTION & SPEED RULES:\n"
                    "1. BOUNDED FETCHING: For broad queries, fetch ONLY the most recent 5 to 10 items in 1 to 2 tool rounds.\n"
                    "2. Keep your final response under 3,500 tokens while preserving all key item details.\n\n"
                    "CRITICAL OUTPUT STRUCTURE RULES:\n"
                    "1. Organize your output into clear bold category headers (e.g., **🚀 Recent Vercel Deployments**, **💬 Recent Slack Messages**, **📂 Notion Databases**).\n"
                    "2. Under each category, list EVERY retrieved item as its own bullet point with its full title/project, status, URL/branch, and timestamp:\n"
                    "   - **[Project / Item Name]** — Status: `Status` | Info: `Details` | Date: `Timestamp`\n"
                    "3. NEVER output single-line pipe tables. Always use multi-line bullet lists with proper newline characters (\\n)."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False
    }

    try:
        # (connect_timeout=10s, read_timeout=180s) for multi-step MCP tool execution
        response = requests.post(HERMES_API_URL, headers=headers, json=payload, timeout=(10, 180))
        response.raise_for_status()
        data = response.json()

        elapsed = round(time.time() - start_ts, 2)
        hermes_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        hermes_reply = format_hermes_markdown(hermes_reply)
        _log(f"[HERMES] RESPONSE RECEIVED in {elapsed}s ({len(hermes_reply)} chars)")
        _log(f"[HERMES FORMATTED PREVIEW]:\n{hermes_reply[:300]}...")
        return hermes_reply if hermes_reply else "Hermes executed the command but returned an empty response."

    except requests.exceptions.ReadTimeout:
        elapsed = round(time.time() - start_ts, 2)
        _log(f"[HERMES] TIMEOUT after {elapsed}s on port 8642.")
        return (
            "Hermes Agent timed out while waiting for the external MCP server (Slack/Vercel) to respond. "
            "Try asking for a specific project or channel (e.g., 'Check the latest deployment for KIXX on Vercel')."
        )
    except requests.exceptions.ConnectionError:
        _log("[HERMES] ERROR: Could not connect to Hermes Agent on port 8642.")
        return "System Error: Unable to reach the local Hermes Agent gateway on port 8642. Ensure `hermes gateway` is running."
    except Exception as e:
        _log(f"[HERMES] TOOL ERROR: {e}")
        return f"Error communicating with Hermes Agent: {str(e)}"
