import pytest
from unittest.mock import patch
from app.repositories.case_repository import CaseRepository


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.get_all')
async def test_get_all_cases(mock_get_all):
    """Test getting all cases"""
    mock_cases = [
        {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]},
        {"id": 2, "name": "Case 2", "birthdate": "1990-05-15", "gender": "female", "types": ["type2"]}
    ]
    mock_get_all.return_value = mock_cases

    result = await CaseRepository.get_all_cases()

    mock_get_all.assert_called_once_with("cases")
    assert result == mock_cases


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.get_by_id')
async def test_get_case_by_id(mock_get_by_id):
    """Test getting a case by ID"""
    mock_case = {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}
    mock_get_by_id.return_value = mock_case

    result = await CaseRepository.get_case_by_id(1)

    mock_get_by_id.assert_called_once_with("cases", 1)
    assert result == mock_case


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.create')
async def test_create_case(mock_create):
    """Test creating a case"""
    mock_case = {
        "id": 1,
        "name": "Case 1",
        "birthdate": "2000-01-01",
        "caseDescription": "Description",
        "gender": "male",
        "types": ["type1"]
    }
    mock_create.return_value = mock_case

    case_data = {
        "name": "Case 1",
        "birthdate": "2000-01-01",
        "caseDescription": "Description",
        "gender": "male",
        "types": ["type1"]
    }

    result = await CaseRepository.create_case(case_data)

    mock_create.assert_called_once_with("cases", case_data)
    assert result == mock_case


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.update')
async def test_update_case(mock_update):
    """Test updating a case"""
    mock_case = {
        "id": 1,
        "name": "Updated Case",
        "birthdate": "2000-01-01",
        "caseDescription": "Updated Description",
        "gender": "male",
        "types": ["type1"]
    }
    mock_update.return_value = mock_case

    case_data = {
        "name": "Updated Case",
        "caseDescription": "Updated Description"
    }

    result = await CaseRepository.update_case(1, case_data)

    mock_update.assert_called_once_with("cases", 1, case_data)
    assert result == mock_case


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.delete')
async def test_delete_case(mock_delete):
    """Test deleting a case"""
    mock_delete.return_value = True

    result = await CaseRepository.delete_case(1)

    mock_delete.assert_called_once_with("cases", 1)
    assert result is True