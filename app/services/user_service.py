from typing import List, Dict, Optional
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository, UserDict
from app.models.user import (
    UserCreate, UserUpdate, AdminUserUpdate
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
    async def admin_update_user(user_id: int, user_data: AdminUserUpdate, current_user_id: int) -> UserDict:
        """Admin update user information - unified method for all admin updates"""
        try:
            # Check if user exists
            user = await UserService.get_user_by_id(user_id)
            print(f"Found user: {user}")
            
            # If email is changing, check if new email is already taken
            if user_data.email and user_data.email != user["email"]:
                existing_user = await UserRepository.get_user_by_email(user_data.email)
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
            
            # Business logic validations
            
            # Prevent admin from removing their own admin privileges
            if user_id == current_user_id and user_data.isAdmin is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin users cannot remove their own admin privileges"
                )
            
            # Prevent admin from deactivating their own account
            if user_id == current_user_id and user_data.activate is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin users cannot deactivate their own account"
                )
            
            # Prepare update data
            update_data = {k: v for k, v in user_data.model_dump().items() if v is not None}
            print(f"Update data: {update_data}")
            
            if not update_data:
                return user
            
            # Handle password update separately if provided
            if "new_password" in update_data:
                # Remove password from update_data and handle it separately
                new_password = update_data.pop("new_password")
                
                # Update other fields first if any
                if update_data:
                    updated_user = await UserRepository.update_user(user_id, update_data)
                    if not updated_user:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to update user"
                        )
                
                # Update password
                updated_user = await UserRepository.update_password(user_id, new_password)
                if not updated_user:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to update password"
                    )
            else:
                # Update user without password change
                updated_user = await UserRepository.update_user(user_id, update_data)
                if not updated_user:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to update user"
                    )
            
            print(f"Updated user: {updated_user}")
            return updated_user
        except Exception as e:
            print(f"Error in admin_update_user: {e}")
            raise e

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> UserDict:
        """Update user information (for regular users) - unified method for name, email, and password"""
        try:
            # Check if user exists
            user = await UserService.get_user_by_id(user_id)
            print(f"Found user: {user}")
            
            # If email is changing, check if new email is already taken
            if user_data.email and user_data.email != user["email"]:
                existing_user = await UserRepository.get_user_by_email(user_data.email)
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
            
            # Handle password validation if both old and new password are provided
            if user_data.new_password:
                if not user_data.old_password:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Old password is required when updating password"
                    )
                
                # Verify old password
                if not UserRepository.verify_password(user_data.old_password, user["password"]):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect old password"
                    )
            
            # Prepare update data (exclude password fields)
            update_data = {}
            if user_data.name is not None:
                update_data["name"] = user_data.name
            if user_data.email is not None:
                update_data["email"] = user_data.email
            
            print(f"Update data: {update_data}")
            
            # Update basic fields if any
            updated_user = user
            if update_data:
                updated_user = await UserRepository.update_user(user_id, update_data)
                if not updated_user:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to update user"
                    )
            
            # Update password if provided
            if user_data.new_password:
                updated_user = await UserRepository.update_password(user_id, user_data.new_password)
                if not updated_user:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to update password"
                    )
            
            print(f"Updated user: {updated_user}")
            return updated_user
        except Exception as e:
            print(f"Error in update_user: {e}")
            raise e

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
