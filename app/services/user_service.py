from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.models.user import UserCreate, UserUpdate, UserUpdatePassword, UserUpdateRole


class UserService:
    @staticmethod
    async def get_all_users() -> List[Dict[str, Any]]:
        """Get all users"""
        return await UserRepository.get_all_users()
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID"""
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> Dict[str, Any]:
        """Create a new user"""
        # Check if email already exists
        existing_user = await UserRepository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user_dict = user_data.model_dump()
        return await UserRepository.create_user(user_dict)
    
    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> Dict[str, Any]:
        """Update user information"""
        # Check if user exists
        user = await UserService.get_user_by_id(user_id)
        
        # If email is changing, check if new email is already taken
        if user_data.email and user_data.email != user["email"]:
            existing_user = await UserRepository.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Update user
        update_data = {k: v for k, v in user_data.model_dump().items() if v is not None}
        if not update_data:
            return user
        
        updated_user = await UserRepository.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
        return updated_user
    
    @staticmethod
    async def update_user_role(user_id: int, role_data: UserUpdateRole) -> Dict[str, Any]:
        """Update user role (admin only)"""
        # Check if user exists
        await UserService.get_user_by_id(user_id)
        
        # Update role
        update_data = {k: v for k, v in role_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        updated_user = await UserRepository.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user role"
            )
        return updated_user
    
    @staticmethod
    async def update_password(
        user_id: int, 
        password_data: UserUpdatePassword
    ) -> Dict[str, Any]:
        """Update user password"""
        # Check if user exists
        user = await UserService.get_user_by_id(user_id)
        
        # Verify old password
        if not UserRepository.verify_password(
            password_data.old_password, 
            user["password"]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        
        # Update password
        updated_user = await UserRepository.update_password(
            user_id, 
            password_data.new_password
        )
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        return {"message": "Password updated successfully"}
