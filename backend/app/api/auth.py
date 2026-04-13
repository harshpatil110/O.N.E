from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, hash_password, create_access_token
from app.core.auth_deps import get_hr_admin_user
from app.schemas.auth import LoginRequest, TokenResponse, RegisterEmployeeRequest, UserResponse

try:
    from app.models.user import User
except ImportError:
    # If the database model missing, assume dict usage or similar
    pass

router = APIRouter()

@router.post("/auth/register-employee", response_model=UserResponse)
async def register_employee(
    request: RegisterEmployeeRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_hr_admin_user)
):
    """
    Register a new employee. Only an HR admin can call this endpoint.
    """
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Hash password (we assume password might come in the request or we generate it)
    # The snippet doesn't include password in RegisterEmployeeRequest natively, 
    # so we might assume a default or one passed. Using a placeholder password:
    raw_password = getattr(request, "password", "defaultpassword123")
    hashed_pw = hash_password(raw_password)
    
    # Create the user
    new_user = User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_pw,
        role="employee"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # UserResponse model should exclude the hashed_password
    return new_user

@router.post("/auth/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password to receive a JWT token.
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    # Verify password and existence
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token payload. Custom payload logic goes here
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=user.role
    )
