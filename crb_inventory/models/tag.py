from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TagModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TagListResponse(BaseModel):
    result: List[TagModel]
    total: int
    page: int
    page_size: int


class TagResponse(BaseModel):
    result: TagModel


class TagCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class TagUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
