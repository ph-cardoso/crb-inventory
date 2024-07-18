from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ..models.validators import validate_custom_field_name_value


class CustomFieldModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomFieldListResponse(BaseModel):
    result: List[CustomFieldModel]
    total: int
    page: int
    page_size: int


class CustomFieldResponse(BaseModel):
    result: CustomFieldModel


class CustomFieldCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

    _validate_custom_field_name_value = field_validator("name", mode="after")(
        validate_custom_field_name_value
    )


class CustomFieldUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool

    _validate_custom_field_name_value = field_validator("name", mode="after")(
        validate_custom_field_name_value
    )
