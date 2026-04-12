import pytest
from app.core.fsm import FSMState
from app.core.state import ConversationState
from app.agents.fsm_controller import FSMController
from app.core.exceptions import InvalidTransitionError

def test_valid_transitions():
    state = ConversationState(session_id="s1", user_id="u1")
    fsm = FSMController(state)
    
    assert fsm.state.current_fsm_state == FSMState.WELCOME
    
    fsm.transition(FSMState.PROFILING)
    assert fsm.state.current_fsm_state == FSMState.PROFILING
    
    fsm.transition(FSMState.PLAN_GENERATION)
    assert fsm.state.current_fsm_state == FSMState.PLAN_GENERATION
    
    fsm.transition(FSMState.ONBOARDING_EXECUTION)
    assert fsm.state.current_fsm_state == FSMState.ONBOARDING_EXECUTION
    
    fsm.transition(FSMState.CHECKLIST_REVIEW)
    assert fsm.state.current_fsm_state == FSMState.CHECKLIST_REVIEW
    
    fsm.transition(FSMState.COMPLETED)
    assert fsm.state.current_fsm_state == FSMState.COMPLETED

def test_invalid_transition_raises_error():
    state = ConversationState(session_id="s1", user_id="u1")
    fsm = FSMController(state)
    
    with pytest.raises(InvalidTransitionError):
        fsm.transition(FSMState.ONBOARDING_EXECUTION)

def test_free_qa_transitions():
    state = ConversationState(session_id="s1", user_id="u1", current_fsm_state=FSMState.ONBOARDING_EXECUTION)
    fsm = FSMController(state)
    
    fsm.transition(FSMState.FREE_QA)
    assert fsm.state.current_fsm_state == FSMState.FREE_QA
    
    # Check return to ONBOARDING_EXECUTION
    fsm.transition(FSMState.ONBOARDING_EXECUTION)
    assert fsm.state.current_fsm_state == FSMState.ONBOARDING_EXECUTION

def test_should_transition_from_welcome():
    state = ConversationState(session_id="s1", user_id="u1")
    fsm = FSMController(state)
    
    assert fsm.should_transition("", {}) is None
    
    state.persona = {"name": "Jane"}
    assert fsm.should_transition("", {}) is None
    
    # Requirement: name and email -> switch to profiling
    state.persona = {"name": "Jane", "email": "jane@example.com"}
    assert fsm.should_transition("", {}) == FSMState.PROFILING

def test_should_transition_from_profiling():
    state = ConversationState(session_id="s1", user_id="u1", current_fsm_state=FSMState.PROFILING)
    fsm = FSMController(state)
    
    state.persona = {"name": "Jane", "email": "jane@example.com", "role": "frontend", "level": "senior", "tech_stack": ["React"]}
    assert fsm.should_transition("", {}) is None
    
    state.persona["team"] = "Alpha"
    assert fsm.should_transition("", {}) == FSMState.PLAN_GENERATION

def test_should_transition_from_onboarding():
    state = ConversationState(session_id="s1", user_id="u1", current_fsm_state=FSMState.ONBOARDING_EXECUTION)
    fsm = FSMController(state)
    
    state.checklist = [
        {"item_key": "x", "required": True, "status": "completed"},
        {"item_key": "y", "required": True, "status": "pending"}
    ]
    assert fsm.should_transition("", {}) is None
    
    state.checklist[1]["status"] = "skipped"
    assert fsm.should_transition("", {}) == FSMState.CHECKLIST_REVIEW
