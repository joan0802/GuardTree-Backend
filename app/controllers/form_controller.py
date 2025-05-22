from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Type, Literal
from app.core.auth import get_current_user, get_current_admin_user
from app.models.form_entry import FormEntry, FormEntryCreate
from app.services.form_service import FormService

router = APIRouter(prefix="/forms", tags=["forms"])

@router.get("/", response_model=List[FormEntry])
async def get_all(current_user: dict = Depends(get_current_user)):
    return await FormService.get_all()

@router.get("/{form_id}")
async def get_by_id(form_id: int, current_user: dict = Depends(get_current_user)):
    return await FormService.get_by_id(form_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(form_data: FormEntryCreate, current_user: dict = Depends(get_current_user)):
    return await FormService.create(form_data.dict())

@router.delete("/{form_id}")
async def delete(form_id: int, current_user: dict = Depends(get_current_admin_user)):
    return await FormService.delete(form_id)

@router.post("/{form_type}/", status_code=status.HTTP_201_CREATED)
async def create_with_type(form_type: Literal["A", "B", "C", "D", "E", "F", "G"], form_data: FormEntryCreate, current_user: dict = Depends(get_current_user)):
    data = form_data.copy(update={"source_form": form_type})
    return await FormService.create(data.dict())