from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import date

class DeveloperPersona(BaseModel):
    name: str
    email: str
    start_date: Optional[date] = None
    role: Literal["backend", "frontend", "devops", "fullstack", "data"]
    experience_level: Literal["intern", "junior", "mid", "senior"]
    tech_stack: List[str]  # e.g. ["python", "django", "postgres"]
    team: Optional[str] = None
    
    def is_complete(self) -> bool:
        return all([self.name, self.email, self.role, 
                    self.experience_level, self.tech_stack])
