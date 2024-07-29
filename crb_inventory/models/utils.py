from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AppResource(Enum):
    CATEGORY = "category"
    TAG = "tag"
    ITEM = "item"


class ResourceDeletedMessage(BaseModel):
    message: Optional[str] = "Resource deleted successfully."
    id: str
    resource: AppResource
