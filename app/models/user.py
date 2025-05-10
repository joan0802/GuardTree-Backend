from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = "user"
    isAdmin: bool = False


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str


class UserUpdateRole(BaseModel):
    role: str
    isAdmin: Optional[bool] = None


class User(UserBase):
    id: int
    role: str
    created_at: datetime
    isAdmin: bool

    class Config:
        from_attributes = True 