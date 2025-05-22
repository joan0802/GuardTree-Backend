import pytest
from app.repositories.form_repository import FormRepository

@pytest.fixture
def form_record_data():
    import json
    with open("app/data/form_filled_template.json", encoding="utf-8") as f:
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
async def test_repo_crud(form_record_data):
    # Create
    created = await FormRepository.create(form_record_data)
    form_id = created["id"]
    assert created["form_A"][0]["activity"] == form_record_data["form_A"][0]["activity"]

    # Get by id
    got = await FormRepository.get_by_id(form_id)
    assert got["id"] == form_id

    # Get all
    all_forms = await FormRepository.get_all()
    assert any(f["id"] == form_id for f in all_forms)

    # Delete
    deleted = await FormRepository.delete(form_id)
    assert deleted

    # Confirm delete
    got = await FormRepository.get_by_id(form_id)
    assert got is None
