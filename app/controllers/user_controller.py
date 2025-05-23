from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.models.user import UserCreate, UserUpdate, User, UserUpdatePassword, UserUpdateRole
from app.services.user_service import UserService
from app.core.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["users"])

# Admin routes
@router.get("/", response_model=List[User])
async def get_all_users(current_user: Dict[str, Any] = Depends(get_current_admin_user)):
    """
    Get all users (admin only)
    """
    return await UserService.get_all_users()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: Dict[str, Any] = Depends(get_current_admin_user)
):
    """
    Create a new user (admin only)
    """
    return await UserService.create_user(user_data)

# Regular user routes - specific paths first
@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get current user's information
    """
    return await UserService.get_user_by_id(current_user["id"])

@router.put("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update current user's information
    """
    return await UserService.update_user(current_user["id"], user_data)

@router.put("/me/password")
async def update_current_user_password(
    password_data: UserUpdatePassword,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update current user's password
    """
    return await UserService.update_password(current_user["id"], password_data)

# Admin routes with parameters - put after specific paths
@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_admin_user)
):
    """
    Get a specific user by ID (admin only)
    """
    return await UserService.get_user_by_id(user_id)

@router.put("/{user_id}/role", response_model=User)
async def update_user_role(
    user_id: int,
    role_data: UserUpdateRole,
    current_user: Dict[str, Any] = Depends(get_current_admin_user)
):
    """
    Update a user's role (admin only)
    """
    return await UserService.update_user_role(user_id, role_data)

@router.put("/{user_id}/activate", response_model=User)
async def update_user_activation(
    user_id: int,
    activate: bool,
    current_user: Dict[str, Any] = Depends(get_current_admin_user)
):
    """
    Activate or deactivate a user (admin only)
    """
    user_data = UserUpdate(activate=activate)
    return await UserService.update_user(user_id, user_data)