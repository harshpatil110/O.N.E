from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.config import settings
from app.core.database import get_db
# Mocking the User import if missing. Adjust import paths based on your actual models
try:
    from app.models.user import User
except ImportError:
    # Fallback to schema if model doesn't exist yet
    from app.schemas.auth import UserResponse as User

# The URL here should match your login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Validate the JWT token, extract the user ID, and return the DB User object.
    Raises 401 Unauthorized if the token is invalid or the user cannot be found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        # Fallback if the User model doesn't support query directly
        raise credentials_exception

async def get_hr_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency that ensures the current user has HR Admin or Superadmin privileges.
    Raises 403 Forbidden otherwise.
    """
    if current_user.role not in ["hr_admin", "superadmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="HR admin access required"
        )
    return current_user
