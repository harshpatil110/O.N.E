from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    HR_ADMIN = "hr_admin"
    ENG_MANAGER = "eng_manager"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class RegisterEmployeeRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.EMPLOYEE

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    
    model_config = {"from_attributes": True}
