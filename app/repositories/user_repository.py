from typing import List, Dict, Any, Optional
import bcrypt
from app.core.supabase_client import SupabaseService


class UserRepository:
    TABLE_NAME = "users"
    
    @staticmethod
    async def get_all_users() -> List[Dict[str, Any]]:
        """Get all users from the database"""
        return await SupabaseService.get_all(UserRepository.TABLE_NAME)
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific user by ID"""
        return await SupabaseService.get_by_id(UserRepository.TABLE_NAME, user_id)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email"""
        response = await SupabaseService.query(
            UserRepository.TABLE_NAME, 
            filters={"email": email}
        )
        return response[0] if response else None
    
    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        # Hash the password before storing
        user_data["password"] = UserRepository._hash_password(user_data["password"])
        return await SupabaseService.create(UserRepository.TABLE_NAME, user_data)
    
    @staticmethod
    async def update_user(user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        return await SupabaseService.update(UserRepository.TABLE_NAME, user_id, user_data)
    
    @staticmethod
    async def update_password(user_id: int, new_password: str) -> Dict[str, Any]:
        """Update user password"""
        hashed_password = UserRepository._hash_password(new_password)
        return await SupabaseService.update(
            UserRepository.TABLE_NAME, 
            user_id, 
            {"password": hashed_password}
        )
    
    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete a user"""
        return await SupabaseService.delete(UserRepository.TABLE_NAME, user_id)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        ) 
    

if __name__ == "__main__":
    print(UserRepository._hash_password("guardtree2025"))