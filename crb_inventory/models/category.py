from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CategoryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CategoryListResponse(BaseModel):
    result: List[CategoryModel]
    total: int
    page: int
    page_size: int


class CategoryResponse(BaseModel):
    result: CategoryModel


class CategoryCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
