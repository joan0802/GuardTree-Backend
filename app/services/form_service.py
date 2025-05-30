from fastapi import HTTPException
from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.form_repository import FormRepository

class FormService:
    @staticmethod
    async def get_all():
        records = await FormRepository.get_all()
        # batch find name (can be optimized to find all case/user at once)
        for r in records:
            case = await CaseRepository.get_case_by_id(r["case_id"])
            user = await UserRepository.get_user_by_id(r["user_id"])
            r["case_name"] = case["name"] if case else None
            r["user_name"] = user["name"] if user else None
        return records

    @staticmethod
    async def get_by_id(form_id):
        record = await FormRepository.get_by_id(form_id)
        if not record:
            raise HTTPException(status_code=404, detail="Form not found")
        # find case/user name
        case = await CaseRepository.get_case_by_id(record["case_id"])
        user = await UserRepository.get_user_by_id(record["user_id"])
        record["case_name"] = case["name"] if case else None
        record["user_name"] = user["name"] if user else None
        return record

    @staticmethod
    async def create(data):
        case_id = data["case_id"]
        user_id = data["user_id"]
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(status_code=400, detail="case_id not found")
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user_id not found")
        return await FormRepository.create(data)

    @staticmethod
    async def delete(form_id: int):
        form = await FormRepository.get_by_id(form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        await FormRepository.delete(form_id)
        return {"message": "Deleted successfully"}

    @staticmethod
    async def update(form_id, data):
        case_id = data["case_id"]
        user_id = data["user_id"]
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(status_code=400, detail="case_id not found")
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=400, detail="user_id not found")
        return await FormRepository.update(form_id, data)