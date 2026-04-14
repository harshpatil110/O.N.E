from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    HR_ADMIN = "hr_admin"
    ENG_MANAGER = "eng_manager"

class LoginRequest(BaseModel):
    """Payload for user login."""
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "dev@company.com",
                "password": "securepassword123"
            }
        }
    )

class TokenResponse(BaseModel):
    """Response containing JWT access token."""
    access_token: str
    token_type: str = "bearer"
    role: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "role": "employee"
            }
        }
    )

class RegisterEmployeeRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.EMPLOYEE

class UserResponse(BaseModel):
    """Public user profile information."""
    id: str
    name: str
    email: EmailStr
    role: str
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "user_789",
                "name": "HR Specialist",
                "email": "hr@company.com",
                "role": "hr_admin"
            }
        }
    )
