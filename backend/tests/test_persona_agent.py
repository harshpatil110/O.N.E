import pytest
import os
from dotenv import load_dotenv
load_dotenv()
from app.agents.persona_agent import PersonaAgent
from app.services.llm_service import LLMService

test_cases = [
    {
        "input": "Hi I'm Jane Doe, jane@company.com. I'm a senior backend developer mostly working with Python and Go.",
        "expected": {
            "name": "Jane Doe",
            "email": "jane@company.com",
            "role": "backend",
            "experience_level": "senior",
            "tech_stack": ["python", "go"]
        }
    },
    {
        "input": "I'm Alex, alex@company.com, a junior frontend dev. I mainly use React and TypeScript.",
        "expected": {
            "name": "Alex",
            "email": "alex@company.com",
            "role": "frontend",
            "experience_level": "junior",
            "tech_stack": ["react", "typescript"]
        }
    },
    {
        "input": "Intern here! My name is Rahul Sharma, rahul@company.com. I'm just starting out with Python.",
        "expected": {
            "name": "Rahul Sharma",
            "email": "rahul@company.com",
            # The logic maps default undefined roles, but python typically falls to backend or data.
            # We'll check only keys present in expected
            "experience_level": "intern",
            "tech_stack": ["python"]
        }
    }
]

@pytest.mark.asyncio
async def test_extract_persona():
    # Will make live API calls. Ensure API key is set.
    llm_service = LLMService()
    agent = PersonaAgent(llm_service)
    
    for idx, case in enumerate(test_cases):
        history = [{"role": "user", "content": case["input"]}]
        result = await agent.extract_persona(history)
        
        for k, v in case["expected"].items():
            actual = result.get(k)
            if isinstance(v, list):
                assert actual is not None
                # lower case checks for stacks
                assert sorted([s.lower() for s in actual]) == sorted([s.lower() for s in v])
            else:
                assert actual == v

@pytest.mark.asyncio
async def test_check_profiling_complete():
    agent = PersonaAgent(None) # don't need llm
    
    assert await agent.check_profiling_complete({
        "name": "John", "email": "a@b.c", "role": "backend", 
        "experience_level": "mid", "tech_stack": ["java"]
    }) is True
    
    # Missing stack
    assert await agent.check_profiling_complete({
        "name": "John", "email": "a@b.c", "role": "backend", 
        "experience_level": "mid", "tech_stack": None
    }) is False

@pytest.mark.asyncio
async def test_get_next_profiling_question():
    agent = PersonaAgent(None)
    
    q1 = await agent.get_next_profiling_question({})
    assert "name" in q1.lower()
    
    q2 = await agent.get_next_profiling_question({"name": "A", "email": "a@b.c"})
    assert "role" in q2.lower()
