from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ..models.validators import validate_tag_name_value


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

    _validate_tag_name_value = field_validator("name", mode="after")(
        validate_tag_name_value
    )


class TagUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool

    _validate_tag_name_value = field_validator("name", mode="after")(
        validate_tag_name_value
    )


class TagPatchRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    _validate_tag_name_value = field_validator("name", mode="after")(
        validate_tag_name_value
    )
