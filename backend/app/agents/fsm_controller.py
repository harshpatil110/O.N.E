import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from app.core.fsm import FSMState, VALID_TRANSITIONS
from app.core.state import ConversationState
from app.core.prompts import SYSTEM_PROMPTS
from app.core.exceptions import InvalidTransitionError

logger = logging.getLogger(__name__)

class FSMController:
    def __init__(self, session_state: ConversationState):
        self.state = session_state

    def can_transition(self, to_state: FSMState) -> bool:
        allowed = VALID_TRANSITIONS.get(self.state.current_fsm_state, [])
        return to_state in allowed

    def transition(self, to_state: FSMState) -> None:
        if not self.can_transition(to_state):
            raise InvalidTransitionError(f"Cannot transition from {self.state.current_fsm_state.value} to {to_state.value}")
        
        logger.info(f"FSM Transition: {self.state.current_fsm_state.value} -> {to_state.value} [Session: {self.state.session_id}]")
        self.state.current_fsm_state = to_state
        self.state.last_active = datetime.now(timezone.utc)

    def get_system_prompt_for_state(self, **kwargs) -> str:
        prompt_template = SYSTEM_PROMPTS.get(self.state.current_fsm_state, "")
        
        # Master defaults for every known placeholder across all prompt templates.
        # This prevents KeyError crashes when a template references a variable
        # that the caller didn't supply (e.g. {filename} in citation instructions).
        safe_args = {
            "developer_name": "Developer",
            "role": "Unknown",
            "experience_level": "Unknown",
            "current_task_title": "Task",
            "current_task_description": "",
            "category": "General",
            "source_documents": "None",
            "filename": "company documents",
            "completed_count": 0,
            "total_count": 0,
        }
        # Overlay caller-provided values on top of defaults
        safe_args.update(kwargs)
        
        try:
            return prompt_template.format(**safe_args)
        except KeyError as e:
            logger.warning(f"Missing prompt placeholder {e} for state {self.state.current_fsm_state.value}. Returning raw template.")
            return prompt_template

    def should_transition(self, agent_response: str, context: Dict[str, Any]) -> Optional[FSMState]:
        current = self.state.current_fsm_state
        
        if current == FSMState.WELCOME:
            persona = self.state.persona
            if persona.get("name") and persona.get("email"):
                return FSMState.PROFILING
                
        elif current == FSMState.PROFILING:
            persona = self.state.persona
            required_keys = ["role", "level", "tech_stack", "team"]
            if all(persona.get(k) for k in required_keys):
                return FSMState.PLAN_GENERATION
                
        elif current == FSMState.PLAN_GENERATION:
            if self.state.checklist:
                return FSMState.ONBOARDING_EXECUTION
                
        elif current == FSMState.ONBOARDING_EXECUTION:
            checklist = self.state.checklist
            if not checklist:
                return None
                
            all_done = all(
                item.get("status") in ["completed", "skipped"]
                for item in checklist if item.get("required", True)
            )
            
            if all_done:
                return FSMState.CHECKLIST_REVIEW
                
        elif current == FSMState.CHECKLIST_REVIEW:
            if context.get("hr_notified", False):
                return FSMState.COMPLETED
                
        return None
