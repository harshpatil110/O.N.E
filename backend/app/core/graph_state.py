from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    State object passed between LangGraph nodes for the O.N.E. Supervisor Agent.
    """
    messages: List[BaseMessage]
    user_id: str
    user_email: str
    user_role: Optional[str]
    progress: int
    current_task: Optional[str]
    next_route: str
