from enum import IntEnum
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

class SupportLevel(int, IntEnum):
    NONE = 0
    MONITOR = 1
    VERBAL = 2
    PARTIAL = 3
    FULL = 4

class FormEntryCreate(BaseModel):
    activity: str
    item: str
    subitem: Optional[str] = None
    support_type: Optional[SupportLevel] = None
    core_area: str
    source_form: Optional[Literal["A", "B", "C", "D", "E", "F", "G"]] = None

class FormEntry(BaseModel):
    id: int
    activity: str
    item: str
    subitem: Optional[str] = None
    support_type: Optional[SupportLevel] = None
    core_area: str
    source_form: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
