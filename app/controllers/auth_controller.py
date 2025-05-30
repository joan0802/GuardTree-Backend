from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict

from app.core.auth import authenticate_user, create_access_token
from app.repositories.user_repository import UserDict

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    """
    Authenticate user and provide JWT token
    """
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Handle case where activate might be None, string, or boolean
    activate = user.get("activate")
    if activate is False or (isinstance(activate, str) and activate.lower() == "false"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": str(user["id"])})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 