from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.case import Case, CaseCreate, CaseUpdate
from app.services.case_service import CaseService
from app.core.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("/", response_model=List[Case])
async def get_all_cases(
    current_user: dict = Depends(get_current_user)
):
    """
    Get all cases
    """
    return await CaseService.get_all_cases()

@router.get("/{case_id}", response_model=Case)
async def get_case(
    case_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific case by ID
    """
    return await CaseService.get_case_by_id(case_id)

@router.post("/", response_model=Case, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new case
    """
    return await CaseService.create_case(case_data.dict())

@router.put("/{case_id}", response_model=Case)
async def update_case(
    case_id: int, case_data: CaseUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a case
    """
    return await CaseService.update_case(case_id, case_data.dict(exclude_unset=True))

@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete a case (admin only)
    """
    return await CaseService.delete_case(case_id)