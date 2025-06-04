from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FormItem(BaseModel):
    activity: str
    item: str
    subitem: Optional[str]
    core_area: str
    support_type: Optional[int]

class FormRecordCreate(BaseModel):
    case_id: int
    user_id: int
    year: int
    form_type: int
    content: List[FormItem]

class FormRecord(FormRecordCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FormRecordResponse(FormRecord):
    case_name: Optional[str] = None
    user_name: Optional[str] = None

class FormMetadata(BaseModel):
    id: int
    case_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    case_name: Optional[str]
    user_name: Optional[str]

class FormRecordUpdate(BaseModel):
    year: Optional[int] = None
    form_type: Optional[int] = None
    content: Optional[List[FormItem]] = None