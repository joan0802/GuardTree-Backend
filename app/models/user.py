from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = "user"
    isAdmin: bool = False
    activate: bool = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None


class AdminUserUpdate(BaseModel):
    """Admin model for updating user information - includes all possible fields"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    isAdmin: Optional[bool] = None
    activate: Optional[bool] = None
    new_password: Optional[str] = None  # Admin can directly set password without old password

class User(UserBase):
    id: int
    role: str
    created_at: datetime
    isAdmin: bool
    activate: bool = True

    class Config:
        from_attributes = True 