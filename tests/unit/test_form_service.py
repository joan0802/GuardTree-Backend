import pytest
from app.services.form_service import FormService
from fastapi import HTTPException
from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.form_repository import FormRepository

@pytest.fixture(autouse=True)
async def setup_case_and_user():
    try:
        await CaseRepository.delete_case(1)
    except Exception:
        pass
    try:
        await UserRepository.delete_user(1)
    except Exception:
        pass
    await CaseRepository.create_case({"id": 1, "name": "測試個案"})
    await UserRepository.create_user({
        "id": 1,
        "name": "測試用戶",
        "password": "test123",
        "role": "user",
        "email": "test@example.com"
    })
    yield

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

@pytest.fixture
def invalid_case_form_record_data(valid_form_record_data):
    d = valid_form_record_data.copy()
    d["case_id"] = 9999  # not exist
    return d

@pytest.fixture
def invalid_user_form_record_data(valid_form_record_data):
    d = valid_form_record_data.copy()
    d["user_id"] = 9999  # not exist
    return d

@pytest.mark.asyncio
async def test_create_get_update_delete(valid_form_record_data):

    print(valid_form_record_data)
    # Create
    created = await FormService.create(valid_form_record_data)
    form_id = created["id"]
    assert created["form_A"][0]["activity"] == valid_form_record_data["form_A"][0]["activity"]

    # Get by id
    got = await FormService.get_by_id(form_id)
    assert got["id"] == form_id

    # Get all
    all_forms = await FormService.get_all()
    assert any(f["id"] == form_id for f in all_forms)
    
    # Delete
    result = await FormService.delete(form_id)
    assert result["message"] == "Deleted successfully"

    # Confirm delete
    with pytest.raises(Exception):
        await FormService.get_by_id(form_id)

@staticmethod
async def create(data):
    case_id = data["case_id"]
    user_id = data["user_id"]
    case = await CaseRepository.get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=400, detail="case_id not found")
    user = await UserRepository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="user_id not found")
    data["case_name"] = case["name"]
    data["user_name"] = user["name"]
    return await FormRepository.create(data)

@pytest.mark.asyncio
async def test_create_success(valid_form_record_data, setup_case_and_user):
    created = await FormService.create(valid_form_record_data)
    assert created["form_A"][0]["activity"] == valid_form_record_data["form_A"][0]["activity"]

@pytest.mark.asyncio
async def test_create_fail_case(invalid_case_form_record_data, setup_case_and_user):
    with pytest.raises(HTTPException) as excinfo:
        await FormService.create(invalid_case_form_record_data)
    assert excinfo.value.detail == "case_id not found"

@pytest.mark.asyncio
async def test_create_fail_user(invalid_user_form_record_data, setup_case_and_user):
    with pytest.raises(HTTPException) as excinfo:
        await FormService.create(invalid_user_form_record_data)
    assert excinfo.value.detail == "user_id not found"
