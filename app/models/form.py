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
    case_name: str
    case_id: int
    user_name: str
    user_id: int
    year: int
    form_A: List[FormItem]
    form_B: List[FormItem]
    form_C: List[FormItem]
    form_D: List[FormItem]
    form_E: List[FormItem]
    form_F: List[FormItem]
    form_G: List[FormItem]

class FormRecord(FormRecordCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True