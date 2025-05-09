from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.core.supabase_client import SupabaseService
from pydantic import BaseModel

router = APIRouter()

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

    class Config:
        from_attributes = True

@router.get("/users", response_model=List[User])
async def get_users(
    limit: Optional[int] = Query(None, description="Limit the number of results"),
    order_by: Optional[str] = Query(None, description="Order by field")
):
    try:
        users = await SupabaseService.query(
            table="users",
            limit=limit,
            order_by=order_by
        )
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    try:
        user = await SupabaseService.get_by_id("users", user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    try:
        new_user = await SupabaseService.create("users", user.model_dump())
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserCreate):
    try:
        updated_user = await SupabaseService.update("users", user_id, user.model_dump())
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        success = await SupabaseService.delete("users", user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 