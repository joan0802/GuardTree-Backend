from fastapi import APIRouter, Depends, status
from typing import List
from app.models.form import FormRecordCreate, FormRecord
from app.services.form_service import FormService

router = APIRouter(prefix="/forms", tags=["forms"])

@router.get("/", response_model=List[FormRecord])
async def get_all():
    return await FormService.get_all()

@router.get("/{form_id}", response_model=FormRecord)
async def get_by_id(form_id: int):
    return await FormService.get_by_id(form_id)

@router.post("/", response_model=FormRecord, status_code=status.HTTP_201_CREATED)
async def create(form_data: FormRecordCreate):
    return await FormService.create(form_data.dict())

@router.delete("/{form_id}")
async def delete(form_id: int):
    return await FormService.delete(form_id)