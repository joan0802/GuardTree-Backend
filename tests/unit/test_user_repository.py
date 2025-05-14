import pytest
import bcrypt
from unittest.mock import patch, AsyncMock

from app.repositories.user_repository import UserRepository


def test_hash_password():
    """Test password hashing"""
    password = "testpassword"
    hashed = UserRepository._hash_password(password)
    
    # Verify it's a bcrypt hash
    assert hashed.startswith("$2b$")
    
    # Verify the password matches the hash
    assert bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def test_verify_password():
    """Test password verification"""
    password = "testpassword"
    hashed = UserRepository._hash_password(password)
    
    # Correct password should verify
    assert UserRepository.verify_password(password, hashed) is True
    
    # Incorrect password should not verify
    assert UserRepository.verify_password("wrongpassword", hashed) is False


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.get_all')
async def test_get_all_users(mock_get_all):
    """Test getting all users"""
    mock_users = [
        {"id": 1, "name": "User 1", "email": "user1@example.com"},
        {"id": 2, "name": "User 2", "email": "user2@example.com"}
    ]
    mock_get_all.return_value = mock_users
    
    result = await UserRepository.get_all_users()
    
    mock_get_all.assert_called_once_with("users")
    assert result == mock_users


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.get_by_id')
async def test_get_user_by_id(mock_get_by_id):
    """Test getting a user by ID"""
    mock_user = {"id": 1, "name": "User 1", "email": "user1@example.com"}
    mock_get_by_id.return_value = mock_user
    
    result = await UserRepository.get_user_by_id(1)
    
    mock_get_by_id.assert_called_once_with("users", 1)
    assert result == mock_user


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.query')
async def test_get_user_by_email(mock_query):
    """Test getting a user by email"""
    mock_user = {"id": 1, "name": "User 1", "email": "user1@example.com"}
    mock_query.return_value = [mock_user]
    
    result = await UserRepository.get_user_by_email("user1@example.com")
    
    mock_query.assert_called_once_with("users", filters={"email": "user1@example.com"})
    assert result == mock_user


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.create')
@patch('app.repositories.user_repository.UserRepository._hash_password')
async def test_create_user(mock_hash_password, mock_create):
    """Test creating a user"""
    mock_hash_password.return_value = "hashed_password"
    mock_user = {
        "id": 1, 
        "name": "New User", 
        "email": "new@example.com",
        "password": "hashed_password"
    }
    mock_create.return_value = mock_user
    
    user_data = {
        "name": "New User",
        "email": "new@example.com",
        "password": "password123"
    }
    
    result = await UserRepository.create_user(user_data)
    
    mock_hash_password.assert_called_once_with("password123")
    assert user_data["password"] == "hashed_password"
    mock_create.assert_called_once_with("users", user_data)
    assert result == mock_user


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.update')
async def test_update_user(mock_update):
    """Test updating a user"""
    mock_user = {
        "id": 1, 
        "name": "Updated User", 
        "email": "user@example.com"
    }
    mock_update.return_value = mock_user
    
    user_data = {"name": "Updated User"}
    
    result = await UserRepository.update_user(1, user_data)
    
    mock_update.assert_called_once_with("users", 1, user_data)
    assert result == mock_user


@pytest.mark.asyncio
@patch('app.core.supabase_client.SupabaseService.delete')
async def test_delete_user(mock_delete):
    """Test deleting a user"""
    mock_delete.return_value = True
    
    result = await UserRepository.delete_user(1)
    
    mock_delete.assert_called_once_with("users", 1)
    assert result is True 