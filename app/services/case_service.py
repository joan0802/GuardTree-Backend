from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.repositories.case_repository import CaseRepository

from app.models.case import Case, CaseCreate, CaseUpdate


class CaseService:
    @staticmethod
    async def get_all_cases() -> List[Case]:
        """Get all cases"""
        return await CaseRepository.get_all_cases()

    @staticmethod
    async def get_case_by_id(case_id: int) -> Case:
        """Get a specific case by ID"""
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case with ID {case_id} not found"
            )
        return case

    @staticmethod
    async def create_case(case_data: CaseCreate) -> Case:
        """Create a new case"""
        case_data = jsonable_encoder(case_data) # deal with date
        return await CaseRepository.create_case(case_data)

    @staticmethod
    async def update_case(case_id: int, case_data: CaseUpdate) -> Case:
        """Update an existing case"""
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case with ID {case_id} not found"
            )
        case_data = jsonable_encoder(case_data)
        updated_case = await CaseRepository.update_case(case_id, case_data)
        if not updated_case:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update case"
            )
        return updated_case

    @staticmethod
    async def delete_case(case_id: int) -> Case:
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