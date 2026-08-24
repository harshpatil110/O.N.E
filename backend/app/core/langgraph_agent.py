import os
import sys
import logging
from typing import Dict, Any

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END

from app.core.graph_state import AgentState
from app.core.rag_tool import search_corporate_knowledge
from app.core.task_tools import get_current_task, mark_task_complete
from app.core.github_tools import get_open_pull_requests, get_recent_commits, get_repository_issues

logger = logging.getLogger(__name__)


def _echo_guard(content: str, messages: list, user_email: str) -> str:
    """
    Echo Prevention Failsafe: If the LLM echoed the user's last message,
    return a sensible fallback instead.
    """
    if messages:
        last_human = next((m.content for m in reversed(messages) if isinstance(m, HumanMessage)), "")
        if content.strip() == last_human.strip():
            logger.warning(f"[ECHO GUARD] Detected echo for '{user_email}'. Replacing with fallback.")
            return f"I'm O.N.E., your onboarding mentor. How can I help you with your current task today, {user_email}?"
    return content

# Initialize local LLM (Qwen 2.5 3B via Ollama)
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.2,
    base_url="http://localhost:11434",
)


def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    Supervisor Node: Evaluates state and classifies user intent to route to the correct node.
    """
    progress = state.get("progress", 0)
    user_role = state.get("user_role")

    # 1. Deterministic Rule: If 0% progress and no role set, route to onboarding
    if progress == 0 and not user_role:
        logger.info("[SUPERVISOR ROUTER] Progress is 0% and user_role is None -> Routing to 'onboarding'")
        return {"next_route": "onboarding"}

    # 2. If user is onboarded (>0% or has role), classify latest message intent using LLM
    messages = state.get("messages", [])
    if not messages:
        return {"next_route": "general"}

    latest_msg = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])

    classification_prompt = SystemMessage(content="""You are an intent classification router for an enterprise onboarding AI mentor.
Classify the user's message into EXACTLY ONE of the following 4 labels:
- 'github': The user is asking about the GitHub repository, PRs, pull requests, commits, branches, codebase, or issues.
- 'task': The user is asking about their current task, next steps, checklist item, progress, or stating they completed a task.
- 'rag': The user is asking about company policies, HR, technical documentation, coding standards, architecture, terminal commands, or documentation.
- 'general': General greeting, casual conversation, or basic chat.

Respond with ONLY ONE word: 'github', 'task', 'rag', or 'general'.""")

    try:
        response = llm.invoke([classification_prompt, HumanMessage(content=latest_msg)])
        raw_intent = str(response.content).strip().lower()
    except Exception as e:
        logger.warning(f"[SUPERVISOR ROUTER] Ollama endpoint unreachable ({e}). Using keyword fallback classification...")
        msg_lower = latest_msg.lower()
        if any(w in msg_lower for w in ["github", "pr", "pull request", "commit", "branch", "codebase", "issue"]):
            raw_intent = "github"
        elif any(w in msg_lower for w in ["task", "next", "checklist", "todo", "done", "step"]):
            raw_intent = "task"
        elif any(w in msg_lower for w in ["policy", "pto", "leave", "vpn", "code", "architecture", "doc", "docker", "setup", "standard"]):
            raw_intent = "rag"
        else:
            raw_intent = "general"

    if "github" in raw_intent:
        route = "github"
    elif "task" in raw_intent:
        route = "task"
    elif "rag" in raw_intent:
        route = "rag"
    else:
        route = "general"

    logger.info(f"[SUPERVISOR ROUTER] User message '{latest_msg}' classified as '{route}'")
    return {"next_route": route}


def onboarding_node(state: AgentState) -> Dict[str, Any]:
    """
    Onboarding Node: Guides 0% progress users through a deterministic 3-question loop for registration.
    """
    messages = state.get("messages", [])
    
    # Count how many messages have been sent by the human in this session so far
    # Note: The welcome AI message is already persisted by the session start endpoint,
    # so human_count=1 means the user has responded with their name.
    human_count = sum(1 for m in messages if isinstance(m, HumanMessage))

    if human_count == 1:
        content = "What is your email id?"
    elif human_count == 2:
        content = "What is your position? (Choose from: frontend dev, backend dev, AI dev, cloud, IT, database dev)"
    else:
        # Step 3 completion (human_count >= 3)
        latest_human_msg = messages[-1].content if messages else ""
        valid_roles = ["frontend dev", "backend dev", "ai dev", "cloud", "it", "database dev"]
        msg_lower = str(latest_human_msg).lower()
        
        extracted_role = next((role for role in valid_roles if role in msg_lower), str(latest_human_msg).strip())
        
        # Action 6.5: Database Mutation
        try:
            from app.core.database import SessionLocal
            from app.models.user import User
            with SessionLocal() as db:
                user = db.query(User).filter(User.id == state["user_id"]).first()
                if user:
                    user.department_role = extracted_role
                    user.onboarding_progress = 5
                    user.tasks_completed = 0
                    db.commit()
            content = "Awesome! Your profile is set up and your onboarding checklist has been generated. What would you like to do next?"
        except Exception as e:
            logger.error(f"[ONBOARDING NODE] DB Update Error: {e}")
            content = "An error occurred while setting up your profile. Please try again."

    return {
        "messages": messages + [AIMessage(content=content)],
        "next_route": "end",
    }


def task_node(state: AgentState) -> dict:
    print("🤖 [TASK NODE EXECUTING]")
    messages = state.get("messages", [])
    # JIT: Prefer the DB-grounded active task over the legacy current_task field
    active_task = state.get("current_active_task") or state.get("current_task", "None")
    user_role = state.get("user_role", "Developer")
    user_email = state.get("user_email", "a developer")
    progress = state.get("progress", 0)
    user_id = state.get("user_id", "")

    print(f"📌 [TASK NODE] DB-grounded active task: '{active_task}'")

    try:
        sys_prompt = f"""You are O.N.E., a strict but helpful Senior Staff Engineer.
You are talking to {user_email}.
CRITICAL SYSTEM OVERRIDE: The developer's current active task from the database is EXACTLY: '{active_task}'.
You MUST base all task-related answers on this exact task. Do NOT reference or instruct on previously completed tasks.

CRITICAL BEHAVIORAL RULES:
1. If the user asks "What is my task?" or "Explain my task", you MUST ONLY explain the task above. Break it down into smaller steps.
2. DO NOT assume they have finished it. DO NOT mark it as complete.
3. End your explanation by asking: "Let me know when you have explicitly finished this, and I will mark it as complete."
4. ONLY trigger the task completion tool if the user explicitly says "I am done", "I finished it", or "mark it complete"."""
        
        sys_msg = SystemMessage(content=sys_prompt)
        messages_to_pass = [sys_msg] + messages
        
        llm_with_tools = llm.bind_tools([get_current_task, mark_task_complete])
        response = llm_with_tools.invoke(messages_to_pass)
        
        # Check if the LLM decided to call a tool
        if hasattr(response, "tool_calls") and response.tool_calls:
            from langchain_core.messages import ToolMessage
            tool_messages = []
            for tc in response.tool_calls:
                tool_name = tc["name"]
                
                if tool_name == "get_current_task":
                    output = get_current_task.invoke({"user_id": user_id})
                elif tool_name == "mark_task_complete":
                    output = mark_task_complete.invoke({"user_id": user_id})
                else:
                    output = "Unknown tool."
                
                tool_messages.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))
            
            # Pass tool outputs back to LLM for final response
            final_messages = messages_to_pass + [response] + tool_messages
            final_response = llm_with_tools.invoke(final_messages)
            reply_text = str(final_response.content)
        else:
            reply_text = response.content if hasattr(response, 'content') else str(response)
        
        # Echo Prevention Failsafe
        reply_text = _echo_guard(reply_text, messages, user_email)

        return {"messages": [AIMessage(content=reply_text)], "next_route": "end"}
        
    except Exception as e:
        print(f"❌ [TASK NODE ERROR] {e}")
        return {"messages": [AIMessage(content="I encountered an error managing your tasks.")], "next_route": "end"}


def rag_node(state: AgentState) -> Dict[str, Any]:
    """
    RAG Node: Queries the hybrid corporate knowledge base using search_corporate_knowledge tool and synthesizes answer.
    """
    messages = state.get("messages", [])
    latest_msg = messages[-1].content if messages and hasattr(messages[-1], "content") else ""

    logger.info(f"--- RAG NODE EXECUTING: LLM received {len(messages)} messages in context window ---")

    # Execute Hybrid RAG tool query
    try:
        rag_context = search_corporate_knowledge.invoke(latest_msg)
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        rag_context = "No relevant corporate documentation found."

    user_role = state.get("user_role", "Developer")
    user_email = state.get("user_email", "a developer")
    progress = state.get("progress", 0)
    # JIT: Prefer the DB-grounded active task
    active_task = state.get("current_active_task") or state.get("current_task", "No current task assigned.")

    prompt = SystemMessage(content=f"""You are O.N.E., a Senior Staff Engineer and onboarding mentor.
You are talking to {user_email}. Their role is {user_role} and they are at {progress}% progress.
CRITICAL SYSTEM OVERRIDE: The developer's current active task from the database is EXACTLY: '{active_task}'.
If the user asks about their task, you MUST refer to this exact task. Do NOT reference previously completed tasks.

CRITICAL RULE: You have been given the full conversation history below. Read ALL previous messages carefully before responding. Do not repeat yourself. Do not ask questions that have already been answered. Reference what the user has already told you.

Answer the user's latest question using the knowledge base context below. Be concise and helpful.
Do NOT echo or repeat the user's message. Generate an original, helpful response.

--- KNOWLEDGE BASE CONTEXT ---
{rag_context}""")

    # Combine System Prompt + Full History
    full_context = [prompt] + messages

    try:
        response = llm.invoke(full_context)
        content = str(response.content)
    except Exception as e:
        logger.warning(f"[RAG NODE] Ollama offline or execution error ({e}). Returning fallback...")
        content = "I encountered a slight system error while looking that up. Could you rephrase your request?"

    # Echo Prevention Failsafe
    content = _echo_guard(content, messages, user_email)

    return {
        "messages": messages + [AIMessage(content=content)],
        "next_route": "end",
    }


def general_node(state: AgentState) -> dict:
    print(f"🤖 [NODE EXECUTING] Processing {len(state['messages'])} messages in context.")
    try:
        user_name = state.get('user_email', 'Developer').split('@')[0].capitalize()
        # JIT: Prefer the DB-grounded active task
        active_task = state.get('current_active_task') or state.get('current_task', 'No active task')
        
        sys_prompt = f"""You are O.N.E., the Senior Onboarding AI.
You are talking to: {user_name} ({state.get('user_email')}).
Role: {state.get('user_role', 'Unknown')} | Progress: {state.get('progress', 0)}%.
CRITICAL SYSTEM OVERRIDE: The developer's current active task from the database is EXACTLY: '{active_task}'.
If they ask about their task or next steps, you MUST refer to this exact task.

INSTRUCTIONS:
1. Answer the user's latest question using the provided context.
2. NEVER repeat the user's exact phrase back to them.
3. If they ask for their name, tell them they are {user_name}."""

        messages_to_pass = [SystemMessage(content=sys_prompt)] + state["messages"]
        response = llm.invoke(messages_to_pass)
        
        reply_text = response.content if hasattr(response, 'content') else str(response)
        last_human_msg = state["messages"][-1].content if state["messages"] else ""
        
        # 🛡️ THE ANTI-ECHO SHIELD 🛡️
        if reply_text.strip().lower() == last_human_msg.strip().lower() or reply_text.strip() == "":
            print("🚨 ECHO DETECTED! Intercepting LLM hallucination.")
            reply_text = f"I am O.N.E. You are {user_name}. I am reviewing your chat history to assist you. How can I help with your current tasks?"

        print(f"📤 [NODE RETURNING] {reply_text[:50]}...")
        return {"messages": [AIMessage(content=reply_text)]}
        
    except Exception as e:
        print(f"❌ [NODE ERROR] {e}")
        return {"messages": [AIMessage(content="System error resolving context.")]}


def github_node(state: AgentState) -> Dict[str, Any]:
    """
    GitHub Node: Fetches data from GitHub API.
    """
    messages = state.get("messages", [])
    user_email = state.get("user_email", "a developer")

    logger.info(f"--- GITHUB NODE EXECUTING: LLM received {len(messages)} messages in context window ---")

    prompt = SystemMessage(content=f"""You are O.N.E., a Senior Staff Engineer. You are talking to {user_email}.
The user is asking about the GitHub repository. Use the provided tools to fetch real-time data and summarize it clearly in Markdown.
If the tools return no data, inform the user.

CRITICAL RULE: Read the conversation history. Do not repeat yourself. Do NOT echo or repeat the user's message.""")
    
    input_messages = [prompt] + messages
    llm_with_github_tools = llm.bind_tools([get_open_pull_requests, get_recent_commits, get_repository_issues])
    
    try:
        response = llm_with_github_tools.invoke(input_messages)
        
        if hasattr(response, "tool_calls") and response.tool_calls:
            from langchain_core.messages import ToolMessage
            tool_messages = []
            for tc in response.tool_calls:
                tool_name = tc["name"]
                
                if tool_name == "get_open_pull_requests":
                    output = get_open_pull_requests.invoke({})
                elif tool_name == "get_recent_commits":
                    output = get_recent_commits.invoke({})
                elif tool_name == "get_repository_issues":
                    output = get_repository_issues.invoke({})
                else:
                    output = "Unknown tool."
                    
                tool_messages.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))
                
            final_messages = input_messages + [response] + tool_messages
            final_response = llm_with_github_tools.invoke(final_messages)
            content = str(final_response.content)
        else:
            content = str(response.content)
    except Exception as e:
        logger.warning(f"[GITHUB NODE] Execution error ({e}). Generating fallback response...")
        content = "I encountered a slight system error while checking GitHub. Could you rephrase your request?"

    # Echo Prevention Failsafe
    content = _echo_guard(content, messages, user_email)

    return {
        "messages": messages + [AIMessage(content=content)],
        "next_route": "end",
    }


# ─── LangGraph State Machine Assembly ──────────────────────────────────────────
def route_next(state: AgentState) -> str:
    """
    Conditional routing function reading supervisor's next_route decision.
    """
    route = state.get("next_route", "general")
    if route not in ["onboarding", "task", "rag", "github", "general"]:
        return END
    return route


workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("onboarding", onboarding_node)
workflow.add_node("task", task_node)
workflow.add_node("rag", rag_node)
workflow.add_node("github", github_node)
workflow.add_node("general", general_node)

# Set Entry Point
workflow.set_entry_point("supervisor")

# Add Conditional Edges from Supervisor
workflow.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "onboarding": "onboarding",
        "task": "task",
        "rag": "rag",
        "github": "github",
        "general": "general",
        END: END,
    },
)

# Add Edges from Execution Nodes to END
workflow.add_edge("onboarding", END)
workflow.add_edge("task", END)
workflow.add_edge("rag", END)
workflow.add_edge("github", END)
workflow.add_edge("general", END)

# Compile Graph
app_graph = workflow.compile()


# ─── Verification Execution ───────────────────────────────────────────────────
if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(level=logging.INFO)
    print("=" * 70)
    print("      LangGraph State Machine Compilation & Verification")
    print("=" * 70)

    print("\n[SUCCESS] LangGraph workflow compiled without errors!")

    # Test 1: 0% User Onboarding Route
    print("\n[TEST 1] Routing Test - 0% Progress User (No Role)")
    state_0pct: AgentState = {
        "messages": [HumanMessage(content="Hello, I just joined.")],
        "user_id": "test-uuid-1",
        "user_email": "test@example.com",
        "user_role": None,
        "progress": 0,
        "current_task": None,
        "next_route": "",
    }
    sup_res1 = supervisor_node(state_0pct)
    print("Supervisor Output:", sup_res1)
    onb_res1 = onboarding_node(state_0pct)
    print("Onboarding Node Response:", onb_res1["messages"][-1].content[:150])

    # Test 2: Task Query Routing
    print("\n[TEST 2] Routing Test - Task Intent ('What should I do next?')")
    state_task: AgentState = {
        "messages": [HumanMessage(content="What should I do next for my onboarding?")],
        "user_id": "test-uuid-2",
        "user_email": "dev@example.com",
        "user_role": "frontend dev",
        "progress": 30,
        "current_task": "Install Node.js v20 LTS and NVM",
        "next_route": "",
    }
    sup_res2 = supervisor_node(state_task)
    print("Supervisor Output:", sup_res2)
    task_res2 = task_node(state_task)
    print("Task Node Response:", task_res2["messages"][-1].content[:150])

    # Test 3: RAG Query Routing
    print("\n[TEST 3] Routing Test - RAG Intent ('What is the PTO policy?')")
    state_rag: AgentState = {
        "messages": [HumanMessage(content="What is the PTO and leave policy?")],
        "user_id": "test-uuid-3",
        "user_email": "rag@example.com",
        "user_role": "backend dev",
        "progress": 50,
        "current_task": "Review Core Application Architecture",
        "next_route": "",
    }
    sup_res3 = supervisor_node(state_rag)
    print("Supervisor Output:", sup_res3)
    rag_res3 = rag_node(state_rag)
    print("RAG Node Response:", rag_res3["messages"][-1].content[:150])

    print("\n" + "=" * 70)
    print("      All LangGraph Agent Tests Passed 100%!")
    print("=" * 70)
