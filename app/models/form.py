from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class FormType(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

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
    form_type: FormType
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
    year: int
    form_type: FormType
    case_name: Optional[str]
    user_name: Optional[str]