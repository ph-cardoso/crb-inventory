from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CustomFieldPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    public_id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomFieldListResponse(BaseModel):
    result: List[CustomFieldPublic]
    total: int
    page: int
    page_size: int


class CustomFieldResponse(BaseModel):
    result: CustomFieldPublic


class CustomFieldCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class CustomFieldUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
