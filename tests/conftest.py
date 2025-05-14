import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
import os
import jwt
from datetime import datetime, timedelta

from app.main import app
from app.core.auth import SECRET_KEY, ALGORITHM
from app.repositories.user_repository import UserRepository


@pytest.fixture
def client() -> Generator:
    """
    Create a test client for the app
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_db(monkeypatch):
    """
    Mock the database operations
    """
    # Sample user data for tests
    test_users = [
        {
            "id": 1,
            "name": "Admin User",
            "email": "admin@example.com",
            "password": UserRepository._hash_password("admin123"),
            "role": "admin",
            "created_at": datetime.now().isoformat(),
            "isAdmin": True
        },
        {
            "id": 2,
            "name": "Test User",
            "email": "user@example.com",
            "password": UserRepository._hash_password("user123"),
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "isAdmin": False
        }
    ]
    
    async def mock_get_all_users():
        return test_users
    
    async def mock_get_user_by_id(user_id: int):
        for user in test_users:
            if user["id"] == user_id:
                return user
        return None
    
    async def mock_get_user_by_email(email: str):
        for user in test_users:
            if user["email"] == email:
                return user
        return None
    
    async def mock_create_user(user_data):
        new_id = max([u["id"] for u in test_users]) + 1
        new_user = {
            "id": new_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "password": user_data["password"],
            "role": user_data.get("role", "user"),
            "created_at": datetime.now().isoformat(),
            "isAdmin": user_data.get("isAdmin", False)
        }
        test_users.append(new_user)
        return new_user
    
    async def mock_update_user(user_id, data):
        for i, user in enumerate(test_users):
            if user["id"] == user_id:
                test_users[i].update(data)
                return test_users[i]
        return None
    
    async def mock_delete_user(user_id):
        for i, user in enumerate(test_users):
            if user["id"] == user_id:
                del test_users[i]
                return True
        return False
    
    # Patch all repository methods
    monkeypatch.setattr(UserRepository, "get_all_users", mock_get_all_users)
    monkeypatch.setattr(UserRepository, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(UserRepository, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(UserRepository, "create_user", mock_create_user)
    monkeypatch.setattr(UserRepository, "update_user", mock_update_user)
    monkeypatch.setattr(UserRepository, "delete_user", mock_delete_user)
    
    return test_users


@pytest.fixture
def admin_token() -> str:
    """
    Create a JWT token for admin user
    """
    token_data = {"sub": str(1)}  # ID of the admin user as a string
    expire = datetime.utcnow() + timedelta(minutes=30)
    token_data.update({"exp": expire})
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


@pytest.fixture
def user_token() -> str:
    """
    Create a JWT token for regular user
    """
    token_data = {"sub": str(2)}  # ID of the regular user as a string
    expire = datetime.utcnow() + timedelta(minutes=30)
    token_data.update({"exp": expire})
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM) 