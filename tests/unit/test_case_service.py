import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.services.case_service import CaseService
from app.repositories.case_repository import CaseRepository

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.get_all_cases")
async def test_get_all_cases(mock_get_all_cases):
    """Test fetching all cases"""
    # Mock repository response
    mock_get_all_cases.return_value = [
        {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]},
        {"id": 2, "name": "Case 2", "birthdate": "1990-05-15", "gender": "female", "types": ["type2"]},
    ]

    # Call service
    result = await CaseService.get_all_cases()

    # Assertions
    mock_get_all_cases.assert_called_once()
    assert len(result) == 2
    assert result[0]["name"] == "Case 1"

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.get_case_by_id")
async def test_get_case_by_id_success(mock_get_case_by_id):
    """Test fetching a case by ID - success"""
    # Mock repository response
    mock_get_case_by_id.return_value = {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}

    # Call service
    result = await CaseService.get_case_by_id(1)

    # Assertions
    mock_get_case_by_id.assert_called_once_with(1)
    assert result["name"] == "Case 1"

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.get_case_by_id")
async def test_get_case_by_id_not_found(mock_get_case_by_id):
    """Test fetching a case by ID - not found"""
    # Mock repository response
    mock_get_case_by_id.return_value = None

    # Call service and expect exception
    with pytest.raises(HTTPException) as excinfo:
        await CaseService.get_case_by_id(1)

    # Assertions
    mock_get_case_by_id.assert_called_once_with(1)
    assert excinfo.value.status_code == 404
    assert "Case with ID 1 not found" in excinfo.value.detail

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.create_case")
async def test_create_case_success(mock_create_case):
    """Test creating a new case"""
    # Mock repository response
    mock_create_case.return_value = {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}

    # Call service
    case_data = {"name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}
    result = await CaseService.create_case(case_data)

    # Assertions
    mock_create_case.assert_called_once_with(case_data)
    assert result["id"] == 1

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.get_case_by_id")
@patch("app.repositories.case_repository.CaseRepository.update_case")
async def test_update_case_success(mock_update_case, mock_get_case_by_id):
    """Test updating an existing case"""
    # Mock repository responses
    mock_get_case_by_id.return_value = {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}
    mock_update_case.return_value = {"id": 1, "name": "Updated Case", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}

    # Call service
    case_data = {"name": "Updated Case", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}
    result = await CaseService.update_case(1, case_data)

    # Assertions
    mock_get_case_by_id.assert_called_once_with(1)
    mock_update_case.assert_called_once_with(1, case_data)
    assert result["name"] == "Updated Case"

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.get_case_by_id")
@patch("app.repositories.case_repository.CaseRepository.delete_case")
async def test_delete_case_success(mock_delete_case, mock_get_case_by_id):
    """Test deleting a case"""
    # Mock repository responses
    mock_get_case_by_id.return_value = {"id": 1, "name": "Case 1", "birthdate": "2000-01-01", "gender": "male", "types": ["type1"]}
    mock_delete_case.return_value = True

    # Call service
    result = await CaseService.delete_case(1)

    # Assertions
    mock_get_case_by_id.assert_called_once_with(1)
    mock_delete_case.assert_called_once_with(1)
    assert result["message"] == "Case deleted successfully"

@pytest.mark.asyncio
@patch("app.repositories.case_repository.CaseRepository.get_case_by_id")
async def test_delete_case_not_found(mock_get_case_by_id):
    """Test deleting a case - not found"""
    # Mock repository response
    mock_get_case_by_id.return_value = None

    # Call service and expect exception
    with pytest.raises(HTTPException) as excinfo:
        await CaseService.delete_case(1)

    # Assertions
    mock_get_case_by_id.assert_called_once_with(1)
    assert excinfo.value.status_code == 404
    assert "Case with ID 1 not found" in excinfo.value.detail