import pytest
from app.services.form_service import FormService
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch

@pytest.fixture
def valid_form_record_data():
    import json
    with open("app/data/form.json", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "case_id": 1,
        "user_id": 1,
        "year": 2024,
        "form_A": data["form_A"],
        "form_B": [],
        "form_C": [],
        "form_D": [],
        "form_E": [],
        "form_F": [],
        "form_G": [],
    }

@pytest.mark.asyncio
async def test_create_success(valid_form_record_data):
    with patch("app.repositories.case_repository.CaseRepository.get_case_by_id", AsyncMock(return_value={"id": 1, "name": "test case"})), \
         patch("app.repositories.user_repository.UserRepository.get_user_by_id", AsyncMock(return_value={"id": 1, "name": "test user"})), \
         patch("app.repositories.form_repository.FormRepository.create", AsyncMock(return_value={"id": 123, **valid_form_record_data})):
        created = await FormService.create(valid_form_record_data)
        assert created["id"] == 123
        assert created["form_A"][0]["activity"] == valid_form_record_data["form_A"][0]["activity"]

@pytest.mark.asyncio
async def test_create_fail_case(valid_form_record_data):
    with patch("app.repositories.case_repository.CaseRepository.get_case_by_id", AsyncMock(return_value=None)), \
         patch("app.repositories.user_repository.UserRepository.get_user_by_id", AsyncMock(return_value={"id": 1, "name": "測試用戶"})):
        with pytest.raises(HTTPException) as excinfo:
            await FormService.create(valid_form_record_data)
        assert excinfo.value.detail == "case_id not found"

@pytest.mark.asyncio
async def test_create_fail_user(valid_form_record_data):
    with patch("app.repositories.case_repository.CaseRepository.get_case_by_id", AsyncMock(return_value={"id": 1, "name": "測試個案"})), \
         patch("app.repositories.user_repository.UserRepository.get_user_by_id", AsyncMock(return_value=None)):
        with pytest.raises(HTTPException) as excinfo:
            await FormService.create(valid_form_record_data)
        assert excinfo.value.detail == "user_id not found"

@pytest.mark.asyncio
async def test_get_by_id_success(valid_form_record_data):
    with patch("app.repositories.form_repository.FormRepository.get_by_id", AsyncMock(return_value={"id": 123, **valid_form_record_data})), \
         patch("app.repositories.case_repository.CaseRepository.get_case_by_id", AsyncMock(return_value={"id": 1, "name": "test case"})), \
         patch("app.repositories.user_repository.UserRepository.get_user_by_id", AsyncMock(return_value={"id": 1, "name": "test user"})):
        got = await FormService.get_by_id(123)
        assert got["id"] == 123
        assert got["case_name"] == "test case"
        assert got["user_name"] == "test user"

@pytest.mark.asyncio
async def test_get_by_id_not_found():
    with patch("app.repositories.form_repository.FormRepository.get_by_id", AsyncMock(return_value=None)):
        with pytest.raises(HTTPException) as excinfo:
            await FormService.get_by_id(999)
        assert excinfo.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_success(valid_form_record_data):
    with patch("app.repositories.form_repository.FormRepository.get_by_id", AsyncMock(return_value={"id": 123, **valid_form_record_data})), \
         patch("app.repositories.form_repository.FormRepository.delete", AsyncMock(return_value=True)):
        result = await FormService.delete(123)
        assert result["message"] == "Deleted successfully"

@pytest.mark.asyncio
async def test_delete_not_found():
    with patch("app.repositories.form_repository.FormRepository.get_by_id", AsyncMock(return_value=None)):
        with pytest.raises(HTTPException) as excinfo:
            await FormService.delete(999)
        assert excinfo.value.status_code == 404