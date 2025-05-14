from typing import List, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.repositories.case_repository import CaseRepository

class CaseService:
    @staticmethod
    async def get_all_cases() -> List[Dict[str, Any]]:
        """Get all cases"""
        return await CaseRepository.get_all_cases()

    @staticmethod
    async def get_case_by_id(case_id: int) -> Dict[str, Any]:
        """Get a specific case by ID"""
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case with ID {case_id} not found"
            )
        return case

    @staticmethod
    async def create_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new case"""
        case_data = jsonable_encoder(case_data) # deal with date
        return await CaseRepository.create_case(case_data)

    @staticmethod
    async def update_case(case_id: int, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing case"""
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case with ID {case_id} not found"
            )
        updated_case = await CaseRepository.update_case(case_id, case_data)
        if not updated_case:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update case"
            )
        return updated_case

    @staticmethod
    async def delete_case(case_id: int) -> Dict[str, str]:
        """Delete a case"""
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case with ID {case_id} not found"
            )
        success = await CaseRepository.delete_case(case_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete case"
            )
        return {"message": "Case deleted successfully"}