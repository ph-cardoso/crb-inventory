from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ..models.validators import validate_positive_value, validate_uuid_value


class ItemModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    category_id: str
    minimum_threshold: int
    stock_quantity: int
    created_at: datetime
    updated_at: datetime


class ItemListResponse(BaseModel):
    result: List[ItemModel]
    total: int
    page: int
    page_size: int


class ItemResponse(BaseModel):
    result: ItemModel


class ItemCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: str
    minimum_threshold: Optional[int] = None
    stock_quantity: Optional[int] = None

    _validate_positive_value = field_validator(
        "minimum_threshold", "stock_quantity", mode="after"
    )(validate_positive_value)

    _validate_uuid_value = field_validator("category_id", mode="after")(
        validate_uuid_value
    )


class ItemUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
    category_id: str
    minimum_threshold: int
    stock_quantity: int

    _validate_positive_value = field_validator(
        "minimum_threshold", "stock_quantity", mode="after"
    )(validate_positive_value)

    _validate_uuid_value = field_validator("category_id", mode="after")(
        validate_uuid_value
    )


class ItemPatchRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[str] = None
    minimum_threshold: Optional[int] = None
    stock_quantity: Optional[int] = None

    _validate_positive_value = field_validator(
        "minimum_threshold", "stock_quantity", mode="after"
    )(validate_positive_value)

    _validate_uuid_value = field_validator("category_id", mode="after")(
        validate_uuid_value
    )
