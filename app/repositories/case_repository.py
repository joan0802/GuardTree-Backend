from typing import List, Dict, Any, Optional
import bcrypt
from app.core.supabase_client import SupabaseService


class CaseRepository:
    TABLE_NAME = "cases"
    
    @staticmethod
    async def get_all_cases() -> List[Dict[str, Any]]:
        """Get all cases from the database"""
        return await SupabaseService.get_all(CaseRepository.TABLE_NAME)
    
    @staticmethod
    async def get_case_by_id(case_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific case by ID"""
        return await SupabaseService.get_by_id(CaseRepository.TABLE_NAME, case_id)
    
    @staticmethod
    async def create_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new case"""
        return await SupabaseService.create(CaseRepository.TABLE_NAME, case_data)
    
    @staticmethod
    async def update_case(case_id: int, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update case information"""
        return await SupabaseService.update(CaseRepository.TABLE_NAME, case_id, case_data)
    
    @staticmethod
    async def delete_case(case_id: int) -> bool:
        """Delete a case"""
        return await SupabaseService.delete(CaseRepository.TABLE_NAME, case_id)
