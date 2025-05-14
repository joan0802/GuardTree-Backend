import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from app.services.user_service import UserService
from app.models.user import UserCreate, UserUpdate, UserUpdatePassword, UserUpdateRole


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.get_all_users')
async def test_get_all_users(mock_get_all_users):
    """Test getting all users"""
    mock_users = [
        {"id": 1, "name": "User 1", "email": "user1@example.com"},
        {"id": 2, "name": "User 2", "email": "user2@example.com"}
    ]
    mock_get_all_users.return_value = mock_users
    
    result = await UserService.get_all_users()
    
    mock_get_all_users.assert_called_once()
    assert result == mock_users


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.get_user_by_id')
async def test_get_user_by_id_success(mock_get_user_by_id):
    """Test getting a user by ID - success case"""
    mock_user = {"id": 1, "name": "User 1", "email": "user1@example.com"}
    mock_get_user_by_id.return_value = mock_user
    
    result = await UserService.get_user_by_id(1)
    
    mock_get_user_by_id.assert_called_once_with(1)
    assert result == mock_user


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.get_user_by_id')
async def test_get_user_by_id_not_found(mock_get_user_by_id):
    """Test getting a user by ID - not found case"""
    mock_get_user_by_id.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        await UserService.get_user_by_id(999)
    
    mock_get_user_by_id.assert_called_once_with(999)
    assert excinfo.value.status_code == 404
    assert "not found" in excinfo.value.detail


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.create_user')
@patch('app.repositories.user_repository.UserRepository.get_user_by_email')
async def test_create_user_success(mock_get_user_by_email, mock_create_user):
    """Test creating a user - success case"""
    # Mock that email doesn't exist yet
    mock_get_user_by_email.return_value = None
    
    # Mock the created user
    mock_user = {
        "id": 1, 
        "name": "New User", 
        "email": "new@example.com",
        "role": "user",
        "isAdmin": False
    }
    mock_create_user.return_value = mock_user
    
    # Create the user
    user_data = UserCreate(
        name="New User",
        email="new@example.com",
        password="password123",
        role="user",
        isAdmin=False
    )
    
    result = await UserService.create_user(user_data)
    
    # Verify the calls
    mock_get_user_by_email.assert_called_once_with("new@example.com")
    mock_create_user.assert_called_once()
    assert result == mock_user


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.get_user_by_email')
async def test_create_user_email_exists(mock_get_user_by_email):
    """Test creating a user - email already exists case"""
    # Mock that email already exists
    mock_get_user_by_email.return_value = {
        "id": 1, 
        "name": "Existing User", 
        "email": "new@example.com"
    }
    
    # Try to create the user with the same email
    user_data = UserCreate(
        name="New User",
        email="new@example.com",
        password="password123"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        await UserService.create_user(user_data)
    
    mock_get_user_by_email.assert_called_once_with("new@example.com")
    assert excinfo.value.status_code == 400
    assert "Email already registered" in excinfo.value.detail


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.update_user')
@patch('app.repositories.user_repository.UserRepository.get_user_by_email')
@patch('app.services.user_service.UserService.get_user_by_id')
async def test_update_user_success(mock_get_user_by_id, mock_get_user_by_email, mock_update_user):
    """Test updating a user - success case"""
    # Mock current user
    mock_get_user_by_id.return_value = {
        "id": 1, 
        "name": "Old Name", 
        "email": "old@example.com"
    }
    
    # Mock that new email doesn't exist
    mock_get_user_by_email.return_value = None
    
    # Mock updated user
    mock_updated_user = {
        "id": 1, 
        "name": "New Name", 
        "email": "new@example.com"
    }
    mock_update_user.return_value = mock_updated_user
    
    # Update the user
    update_data = UserUpdate(name="New Name", email="new@example.com")
    result = await UserService.update_user(1, update_data)
    
    # Verify the calls
    mock_get_user_by_id.assert_called_once_with(1)
    mock_get_user_by_email.assert_called_once_with("new@example.com")
    mock_update_user.assert_called_once()
    assert result == mock_updated_user


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.update_password')
@patch('app.repositories.user_repository.UserRepository.verify_password')
@patch('app.services.user_service.UserService.get_user_by_id')
async def test_update_password_success(mock_get_user_by_id, mock_verify_password, mock_update_password):
    """Test updating a password - success case"""
    # Mock current user
    mock_get_user_by_id.return_value = {
        "id": 1, 
        "name": "User", 
        "email": "user@example.com",
        "password": "hashed_old_password"
    }
    
    # Mock password verification
    mock_verify_password.return_value = True
    
    # Mock password update
    mock_update_password.return_value = {
        "id": 1, 
        "name": "User", 
        "email": "user@example.com",
        "password": "hashed_new_password"
    }
    
    # Update the password
    password_data = UserUpdatePassword(old_password="old_password", new_password="new_password")
    result = await UserService.update_password(1, password_data)
    
    # Verify the calls
    mock_get_user_by_id.assert_called_once_with(1)
    mock_verify_password.assert_called_once_with("old_password", "hashed_old_password")
    mock_update_password.assert_called_once_with(1, "new_password")
    assert result["message"] == "Password updated successfully"


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.verify_password')
@patch('app.services.user_service.UserService.get_user_by_id')
async def test_update_password_incorrect_old_password(mock_get_user_by_id, mock_verify_password):
    """Test updating a password - incorrect old password case"""
    # Mock current user
    mock_get_user_by_id.return_value = {
        "id": 1, 
        "name": "User", 
        "email": "user@example.com",
        "password": "hashed_old_password"
    }
    
    # Mock password verification (fails)
    mock_verify_password.return_value = False
    
    # Update the password
    password_data = UserUpdatePassword(old_password="wrong_password", new_password="new_password")
    
    with pytest.raises(HTTPException) as excinfo:
        await UserService.update_password(1, password_data)
    
    # Verify the calls
    mock_get_user_by_id.assert_called_once_with(1)
    mock_verify_password.assert_called_once_with("wrong_password", "hashed_old_password")
    assert excinfo.value.status_code == 400
    assert "Incorrect password" in excinfo.value.detail


@pytest.mark.asyncio
@patch('app.repositories.user_repository.UserRepository.delete_user')
@patch('app.services.user_service.UserService.get_user_by_id')
async def test_delete_user_success(mock_get_user_by_id, mock_delete_user):
    """Test deleting a user - success case"""
    # Mock user exists
    mock_get_user_by_id.return_value = {
        "id": 1, 
        "name": "User", 
        "email": "user@example.com"
    }
    
    # Mock deletion success
    mock_delete_user.return_value = True
    
    # Delete the user
    result = await UserService.delete_user(1)
    
    # Verify the calls
    mock_get_user_by_id.assert_called_once_with(1)
    mock_delete_user.assert_called_once_with(1)
    assert result["message"] == "User deleted successfully" 