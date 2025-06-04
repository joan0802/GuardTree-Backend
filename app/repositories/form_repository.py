from typing import List, Dict, Any
from app.core.supabase_client import SupabaseService

class FormRepository:
    TABLE_NAME = "forms"
    
    @staticmethod
    async def get_all() -> List[Dict[str, Any]]:
        """Get all form entries from the database"""
        return await SupabaseService.get_all(FormRepository.TABLE_NAME)
   
    @staticmethod
    async def get_by_id(row_id: int):
        """Get a specific form entry by ID"""
        return await SupabaseService.get_by_id(FormRepository.TABLE_NAME, row_id)

    @staticmethod
    async def create(data: dict):
        """Create a new form entry"""
        return await SupabaseService.create(FormRepository.TABLE_NAME, data)

    @staticmethod
    async def delete(row_id: int):
        """Delete a form entry by ID"""
        return await SupabaseService.delete(FormRepository.TABLE_NAME, row_id)

    @staticmethod
    async def get_by_case_id(case_id: int):
        """Get all form entries by case_id"""
        return await SupabaseService.get_by_filter(FormRepository.TABLE_NAME, {"case_id": case_id})

    @staticmethod
    async def update(row_id: int, data: dict):
        """Update a form entry by ID"""
        return await SupabaseService.update(FormRepository.TABLE_NAME, row_id, data)