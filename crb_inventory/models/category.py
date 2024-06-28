from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CategoryPublic(BaseModel):
    public_id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CategoryListResponse(BaseModel):
    result: List[CategoryPublic]
    total: int
    page: int
    page_size: int


class CategoryResponse(BaseModel):
    result: CategoryPublic


class CategoryCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
