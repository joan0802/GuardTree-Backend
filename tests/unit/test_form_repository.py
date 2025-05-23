import pytest
from unittest.mock import AsyncMock, patch
from app.repositories.form_repository import FormRepository

@pytest.fixture
def form_record_data():
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
async def test_create(form_record_data):
    with patch("app.core.supabase_client.SupabaseService.create", AsyncMock(return_value={"id": 1, **form_record_data})):
        created = await FormRepository.create(form_record_data)
        assert created["id"] == 1

@pytest.mark.asyncio
async def test_get_by_id(form_record_data):
    with patch("app.core.supabase_client.SupabaseService.get_by_id", AsyncMock(return_value={"id": 1, **form_record_data})):
        got = await FormRepository.get_by_id(1)
        assert got["id"] == 1

@pytest.mark.asyncio
async def test_get_all(form_record_data):
    with patch("app.core.supabase_client.SupabaseService.get_all", AsyncMock(return_value=[{"id": 1, **form_record_data}])):
        all_forms = await FormRepository.get_all()
        assert any(f["id"] == 1 for f in all_forms)

@pytest.mark.asyncio
async def test_delete():
    with patch("app.core.supabase_client.SupabaseService.delete", AsyncMock(return_value=True)):
        deleted = await FormRepository.delete(1)
        assert deleted
