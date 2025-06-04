from typing import List, Dict, Optional
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository, UserDict
from app.models.user import (
    UserCreate, UserUpdate, UserUpdatePassword, UserUpdateRole,
    UserUpdateActivate, UserUpdateAdmin
)


class UserService:
    @staticmethod
    async def get_all_users() -> List[UserDict]:
        """Get all users"""
        return await UserRepository.get_all_users()
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> UserDict:
        """Get a specific user by ID"""
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserDict:
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
    async def update_user(user_id: int, user_data: UserUpdate) -> UserDict:
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
    async def update_user_role(user_id: int, role_data: UserUpdateRole) -> UserDict:
        """Update user role"""
        # Check if user exists
        await UserService.get_user_by_id(user_id)
        
        # Update role
        update_data = role_data.model_dump()
        updated_user = await UserRepository.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user role"
            )
        return updated_user
    
    @staticmethod
    async def update_user_admin(user_id: int, admin_data: UserUpdateAdmin, current_user_id: int) -> UserDict:
        """Update user admin status"""
        # Check if user exists
        user = await UserService.get_user_by_id(user_id)
        
        # Prevent admin from removing their own admin privileges
        if user_id == current_user_id and not admin_data.isAdmin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin users cannot remove their own admin privileges"
            )
        
        # Update admin status
        update_data = admin_data.model_dump()
        updated_user = await UserRepository.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user admin status"
            )
        return updated_user
    
    @staticmethod
    async def update_user_activate(user_id: int, activate_data: UserUpdateActivate, current_user_id: int) -> UserDict:
        """Update user activation status"""
        # Check if user exists
        user = await UserService.get_user_by_id(user_id)
        
        # Prevent admin from deactivating their own account
        if user_id == current_user_id and not activate_data.activate:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin users cannot deactivate their own account"
            )
        
        # Update activation status
        update_data = activate_data.model_dump()
        updated_user = await UserRepository.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user activation status"
            )
        return updated_user
    
    @staticmethod
    async def update_password(
        user_id: int, 
        password_data: UserUpdatePassword
    ) -> Dict[str, str]:
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

    @staticmethod
    async def delete_user(user_id: int, current_user_id: int) -> Dict[str, str]:
        """Delete a user"""
        # Check if user exists
        user = await UserService.get_user_by_id(user_id)
        
        # Prevent admin from deleting their own account
        if user_id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin users cannot delete their own account"
            )
        
        # Delete user
        success = await UserRepository.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
        return {"message": "User deleted successfully"}

    @staticmethod
    async def admin_update_user_password(
        user_id: int,
        new_password: str,
        current_user_id: int
    ) -> Dict[str, str]:
        """Admin update user password directly"""
        # Check if user exists
        user = await UserService.get_user_by_id(user_id)
        
        # Prevent admin from using this endpoint to change their own password
        if user_id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin should use the regular password update endpoint for their own password"
            )
        
        # Update password
        updated_user = await UserRepository.update_password(
            user_id, 
            new_password
        )
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        return {"message": "Password updated successfully"}
