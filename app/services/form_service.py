from fastapi import HTTPException
from app.repositories.form_repository import FormRepository
from fastapi.encoders import jsonable_encoder

class FormService:
    @staticmethod
    async def get_all():
        return await FormRepository.get_all()

    @staticmethod
    async def get_by_id(row_id: int):
        row = await FormRepository.get_by_id(row_id)
        if not row:
            raise HTTPException(status_code=404, detail=f"Not found")
        return row

    @staticmethod
    async def create(data: dict):
        return await FormRepository.create(jsonable_encoder(data))

    @staticmethod
    async def delete(row_id: int):
        row = await FormRepository.get_by_id(row_id)
        if not row:
            raise HTTPException(status_code=404, detail=f"Not found")
        success = await FormRepository.delete(row_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete")
        return {"message": "Deleted successfully"}
