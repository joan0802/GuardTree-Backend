from pydantic import BaseModel, Field
from typing import Optional, List, Required
from datetime import date, datetime


class CaseBase(BaseModel):
    name: str
    birthdate: date
    caseDescription: Optional[str]
    gender: str
    types: List[str]


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    name: Optional[str] = None
    birthdate: Optional[date] = None
    caseDescription: Optional[str] = None
    gender: Optional[str] = None
    types: Optional[List[str]] = None


class Case(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True