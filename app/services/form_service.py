from fastapi import HTTPException
from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.form_repository import FormRepository

class FormService:
    @staticmethod
    async def get_all():
        records = await FormRepository.get_all()
        for r in records:
            for k in list(r.keys()):
                if k not in ["id", "case_id", "user_id", "year", "form_type", "created_at", "updated_at"]:
                    r.pop(k, None)
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
        create_data = {k: data[k] for k in ["case_id", "user_id", "year", "form_type", "content"] if k in data}
        return await FormRepository.create(create_data)

    @staticmethod
    async def delete(form_id: int):
        form = await FormRepository.get_by_id(form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        await FormRepository.delete(form_id)
        return {"message": "Deleted successfully"}

    @staticmethod
    async def get_by_case_id(case_id):
        case = await CaseRepository.get_case_by_id(case_id)
        if not case:
            raise HTTPException(status_code=400, detail="case_id not found")
        records = await FormRepository.get_by_case_id(case_id)
        for r in records:
            for k in list(r.keys()):
                if k not in ["id", "case_id", "user_id", "year", "form_type", "created_at", "updated_at"]:
                    r.pop(k, None)
            case = await CaseRepository.get_case_by_id(r["case_id"])
            user = await UserRepository.get_user_by_id(r["user_id"])
            r["case_name"] = case["name"] if case else None
            r["user_name"] = user["name"] if user else None
        return records