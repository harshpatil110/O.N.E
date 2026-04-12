from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict

from app.core.fsm import FSMState

def utcnow():
    return datetime.now(timezone.utc)

@dataclass
class ConversationState:
    session_id: str
    user_id: str
    current_fsm_state: FSMState = FSMState.WELCOME
    persona: dict = field(default_factory=dict)
    checklist: list = field(default_factory=list)
    current_checklist_index: int = 0
    conversation_history: List[Dict] = field(default_factory=list)  # last 20 messages
    created_at: datetime = field(default_factory=utcnow)
    last_active: datetime = field(default_factory=utcnow)
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "current_fsm_state": self.current_fsm_state.value,
            "persona": self.persona,
            "checklist": self.checklist,
            "current_checklist_index": self.current_checklist_index,
            "conversation_history": self.conversation_history,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat()
        }
