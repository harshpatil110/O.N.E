from app.services.llm_service import LLMService

PERSONA_EXTRACTION_PROMPT = """
You are extracting a structured developer profile from a conversation.

Given the conversation history below, extract the following fields:
- name: the developer's full name
- email: their email address  
- role: one of [backend, frontend, devops, fullstack, data]
- experience_level: one of [intern, junior, mid, senior]
- tech_stack: a list of technologies (e.g. ["python", "fastapi", "postgres"])
- team: their team name if mentioned, or null

Map natural language to the correct enum values:
- "backend developer", "backend engineer", "server side" → "backend"
- "frontend dev", "UI developer", "React developer" → "frontend"
- "DevOps", "SRE", "infrastructure engineer" → "devops"
- "full stack", "full-stack" → "fullstack"
- "data engineer", "ML engineer", "data scientist" → "data"
- "intern", "trainee" → "intern"
- "junior", "entry level", "1-2 years" → "junior"
- "mid level", "mid-level", "3-5 years" → "mid"
- "senior", "lead", "staff", "principal" → "senior"

Return ONLY a JSON object with these exact keys. No explanation text.
If a field is not yet available, set it to null.

Conversation history:
{conversation_history}
"""

class PersonaAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.output_schema = {
            "type": "object",
            "properties": {
                "name": {"type": ["string", "null"]},
                "email": {"type": ["string", "null"]},
                "role": {"type": ["string", "null"], "enum": ["backend", "frontend", "devops", "fullstack", "data", None]},
                "experience_level": {"type": ["string", "null"], "enum": ["intern", "junior", "mid", "senior", None]},
                "tech_stack": {"type": ["array", "null"], "items": {"type": "string"}},
                "team": {"type": ["string", "null"]}
            },
            "required": ["name", "email", "role", "experience_level", "tech_stack", "team"]
        }

    async def extract_persona(self, conversation_history: list) -> dict:
        # Format conversation history as readable text
        history_text = ""
        for msg in conversation_history:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            history_text += f"{role}: {content}\n"
            
        prompt = PERSONA_EXTRACTION_PROMPT.format(conversation_history=history_text)
        
        # Call llm.extract_structured with PERSONA_EXTRACTION_PROMPT
        extracted = await self.llm.extract_structured(prompt, self.output_schema)
        
        return extracted

    async def check_profiling_complete(self, persona: dict) -> bool:
        # Check if all required fields are non-null
        # Required: name, email, role, experience_level, tech_stack
        required_fields = ["name", "email", "role", "experience_level", "tech_stack"]
        return all(persona.get(field) for field in required_fields)

    async def get_next_profiling_question(self, persona: dict) -> str:
        # Return the next question to ask based on what's missing
        if not persona.get("name") or not persona.get("email"):
            return "What's your name and email address?"
        if not persona.get("role"):
            return "What role are you joining as?"
        if not persona.get("experience_level"):
            return "How would you describe your experience level?"
        if not persona.get("tech_stack"):
            return "What's your primary tech stack?"
        if not persona.get("team"):
            return "Which team are you joining?"
        return "Thank you, I have all the details I need."
