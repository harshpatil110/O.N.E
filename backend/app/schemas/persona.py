from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PersonaRole(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"

class PersonaLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"

class DeveloperPersona(BaseModel):
    name: str
    email: str
    role: Optional[PersonaRole] = None
    level: Optional[PersonaLevel] = None
    tech_stack: list[str] = []
    team: Optional[str] = None
