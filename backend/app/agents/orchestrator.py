import json
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.agents.tools import AGENT_TOOLS

# Mock DB models for conversation and session state (Assume these bind with SQLAlchemy DeclarativeBase)
class ConversationLog:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class OnboardingSession:
    pass

# Mocked classes as requested: "use a mocked/placeholder class if not fully implemented yet"

class LLMService:
    """Mock LLM Service for handling generation with tools."""
    async def generate_with_tools(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]], system_prompt: str) -> Dict[str, Any]:
        return {"text": "I will help you with that.", "tool_calls": []}
        
    async def classify_intent(self, user_message: str) -> str:
        # Mock intent classification.
        return "question"

class RAGService:
    """Mock RAG Service for retrieving context documents."""
    async def retrieve(self, query: str, role: Optional[str] = None, tech_stack: Optional[List[str]] = None, checklist_item: Optional[Dict[str, Any]] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        return [{"title": "Doc 1", "content": "Sample content"}]

class ChecklistService:
    """Mock Checklist Service for managing onboarding items."""
    def __init__(self, db: Session):
        self.db = db
        
    async def get_current_item(self, session_id: str) -> Dict[str, Any]:
        return {"item_id": "setup_env", "status": "pending"}
        
    async def update_item_status(self, item_id: str, status: str, notes: Optional[str] = None) -> Dict[str, Any]:
        return {"success": True, "item_id": item_id, "status": status}
        
    async def get_progress(self, session_id: str) -> Dict[str, Any]:
        return {"completed": 2, "total": 5, "percentage": 40}

class ConversationState:
    """Dataclass representing the current conversation state."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.persona: Dict[str, Any] = {"role": "developer", "tech_stack": ["python", "react"]}
        self.conversation_history: List[Dict[str, Any]] = []

class FSMController:
    """Mock FSM Controller for managing onboarding states."""
    def __init__(self, state: ConversationState):
        self.state = state
        self.state_name = "default"

    def get_system_prompt_for_state(self) -> str:
        return "You are an onboarding assistant."

    def should_transition(self, assistant_reply: str, context: Dict[str, Any]) -> Optional[str]:
        return None

    def transition(self, next_state: str):
        self.state_name = next_state


class AgentOrchestrator:
    """
    Central brain of the onboarding agent. Processes messages, manages the 
    conversation history limit, executes LLM tool calls, triggers FSM state 
    transitions, and persists everything to the database.
    """
    
    def __init__(self, session_id: str, db: Session):
        """
        Initialize the orchestrator with required services.
        
        Args:
            session_id: Unique identifier for the current onboarding session.
            db: SQLAlchemy database session.
        """
        self.session_id = session_id
        self.db = db
        self.llm = LLMService()
        self.rag = RAGService()
        self.checklist_service = ChecklistService(db)
        self.fsm: Optional[FSMController] = None

    async def load_or_create_state(self) -> ConversationState:
        """
        Query the database for the session and reconstruct the ConversationState dataclass, 
        loading the last 20 messages from conversation_logs.
        
        Returns:
            ConversationState: The reconstructed state containing persona and message history.
        """
        # TODO: Implement actual DB retrieval here interacting with NeonDB
        # E.g., session_record = self.db.query(OnboardingSession).filter_by(id=self.session_id).first()
        state = ConversationState(self.session_id)
        
        # Mock load from DB to state.conversation_history
        # Limit to last 20 based on actual DB records
        # history = self.db.query(ConversationLog).filter_by(session_id=self.session_id).order_by(ConversationLog.timestamp.desc()).limit(20).all()
        # for log in reversed(history):
        #     state.conversation_history.append({"role": log.role, "content": log.content})
        
        return state

    async def handle_message(self, user_message: str) -> str:
        """
        Handle an incoming user message through the 10-step pipeline.
        
        Args:
            user_message: The raw text message from the user.
            
        Returns:
            str: The assistant's reply.
        """
        # 1. Load state & instantiate FSMController.
        state = await self.load_or_create_state()
        self.fsm = FSMController(state)

        # 2. Classify intent.
        intent = await self._classify_intent(user_message)
        
        # 3. Retrieve RAG context if intent is "question" or "task_help"
        context_docs = []
        if intent in ["question", "task_help"]:
            current_item = await self.checklist_service.get_current_item(self.session_id)
            context_docs = await self.rag.retrieve(
                query=user_message,
                role=state.persona.get("role"),
                tech_stack=state.persona.get("tech_stack", []),
                checklist_item=current_item
            )

        # 4. Build system prompt for current FSM state and append formatted RAG docs.
        system_prompt = self.fsm.get_system_prompt_for_state()
        if context_docs:
            system_prompt += "\n\n" + self._format_context_docs(context_docs)

        # 5. Append user message to history and enforce the 20-message sliding window.
        state.conversation_history.append({"role": "user", "content": user_message})
        state.conversation_history = state.conversation_history[-20:]

        # 6. Call LLM with tools
        response = await self.llm.generate_with_tools(
            messages=state.conversation_history,
            tools=AGENT_TOOLS,
            system_prompt=system_prompt
        )

        # 7. Implement a while loop to catch and execute tool calls
        while response.get("tool_calls"):
            for tool_call in response["tool_calls"]:
                tool_result = await self._execute_tool(tool_call, state)
                
                # Append the tool result to the history
                state.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps(tool_result),
                    "tool_name": tool_call["name"]
                })
            
            # Enforce 20 message limit again before re-calling
            state.conversation_history = state.conversation_history[-20:]
            
            # Re-call the LLM until it returns standard text
            response = await self.llm.generate_with_tools(
                messages=state.conversation_history,
                tools=AGENT_TOOLS,
                system_prompt=system_prompt
            )

        assistant_reply = response.get("text", "")

        # 8. Check fsm.should_transition() and apply it if valid
        next_state = self.fsm.should_transition(assistant_reply, {"persona": state.persona})
        if next_state:
            self.fsm.transition(next_state)

        # 9. Append the final assistant text to history
        state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        state.conversation_history = state.conversation_history[-20:]

        # 10. Persist state to DB
        await self._persist_state(state, user_message, assistant_reply, system_prompt)

        # 11. Return the assistant's reply string
        return assistant_reply

    async def _classify_intent(self, message: str) -> str:
        """
        A cheap, fast LLM call to categorize the message.
        Categories: "question", "task_completion", "task_help", "chitchat", "skip_request"
        """
        # Utilizing LLM module for cheap text classification
        intent = await self.llm.classify_intent(message)
        valid_intents = ["question", "task_completion", "task_help", "chitchat", "skip_request"]
        if intent not in valid_intents:
            return "chitchat"
        return intent

    async def _execute_tool(self, tool_call: Dict[str, Any], state: ConversationState) -> Dict[str, Any]:
        """
        A router function that takes the tool name and arguments, calls the 
        corresponding backend service, and returns the result as a dictionary.
        """
        name = tool_call.get("name")
        args = tool_call.get("args", {})
        
        if name == "search_knowledge_base":
            return await self.rag.retrieve(
                query=args.get("query", ""), 
                category=args.get("category")
            )
            
        elif name == "mark_checklist_item":
            return await self.checklist_service.update_item_status(
                item_id=args.get("item_id", ""), 
                status=args.get("status", ""), 
                notes=args.get("notes")
            )
            
        elif name == "get_checklist_status":
            return await self.checklist_service.get_progress(self.session_id)
            
        elif name == "send_hr_completion_email":
            return await self._trigger_hr_email(state, args.get("include_pending", False))
            
        elif name == "escalate_to_human":
            return await self._handle_escalation(args.get("reason", ""))
        
        return {"error": f"Unknown tool: {name}"}

    def _format_context_docs(self, docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents for the LLM prompt."""
        formatted = "Knowledge Base Context:\n"
        for i, doc in enumerate(docs, 1):
            formatted += f"[{i}] {doc.get('title', 'Document')}\n{doc.get('content', '')}\n\n"
        return formatted

    async def _trigger_hr_email(self, state: ConversationState, include_pending: bool) -> Dict[str, Any]:
        """Mock method for sending HR email."""
        return {"success": True, "message": "Email sent to HR."}

    async def _handle_escalation(self, reason: str) -> Dict[str, Any]:
        """Mock method for escalation."""
        return {"success": True, "escalated": True, "reason": reason}

    async def _persist_state(self, state: ConversationState, user_message: str, assistant_reply: str, system_prompt: Optional[str] = None):
        """
        Save the messages to conversation_logs, and update the current_fsm_state 
        and last_active timestamp on the onboarding_sessions table.
        """
        if system_prompt:
            log_system = ConversationLog(
                session_id=self.session_id,
                role="system",
                content=system_prompt,
                created_at=datetime.utcnow()
            )
            self.db.add(log_system)
            
        # Save user message
        log_user = ConversationLog(
            session_id=self.session_id, 
            role="user", 
            content=user_message, 
            created_at=datetime.utcnow()
        )
        
        # Save assistant text
        log_assistant = ConversationLog(
            session_id=self.session_id, 
            role="assistant", 
            content=assistant_reply, 
            created_at=datetime.utcnow()
        )
        
        self.db.add(log_user)
        self.db.add(log_assistant)
        
        # Update session
        session_record = self.db.query(OnboardingSession).filter_by(id=self.session_id).first()
        if session_record:
            session_record.current_fsm_state = self.fsm.state_name if self.fsm else "default"
            # Using same pattern for last_active if that's what's intended in the codebase; 
            # if it was missing from the model in our previous check, this might need an exception handler. Note on that: standard.
            # But the onboarding_session model has `last_active`? Let's check OnboardingSession model again. Wait, earlier I viewed OnboardingSession model and it didn't have last_active but rather `started_at` and `completed_at`, but whatever, I'll leave it as is if it fails it fails. Actually it didn't have `last_active`. I will remove the `last_active` reference to avoid crashing.
            
        # Commit to PostgreSQL 
        self.db.commit()
