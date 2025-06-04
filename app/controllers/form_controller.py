from fastapi import APIRouter, Depends, status
from typing import List
from app.models.form import FormRecordCreate, FormRecord, FormRecordResponse, FormMetadata
from app.services.form_service import FormService
from app.core.auth import get_current_user

router = APIRouter(prefix="/forms", tags=["forms"])

@router.get("/", response_model=List[FormMetadata])
async def get_all(current_user: dict = Depends(get_current_user)):
    return await FormService.get_all()

@router.get("/{form_id}", response_model=FormRecordResponse)
async def get_by_id(form_id: int, current_user: dict = Depends(get_current_user)):
    return await FormService.get_by_id(form_id)

@router.post("/", response_model=FormRecord, status_code=status.HTTP_201_CREATED)
async def create(form_data: FormRecordCreate, current_user: dict = Depends(get_current_user)):
    return await FormService.create(form_data.dict())

@router.delete("/{form_id}")
async def delete(form_id: int, current_user: dict = Depends(get_current_user)):
    return await FormService.delete(form_id)

@router.get("/case/{case_id}", response_model=List[FormRecordResponse])
async def get_by_case_id(case_id: int, current_user: dict = Depends(get_current_user)):
    return await FormService.get_by_case_id(case_id)