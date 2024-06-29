from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AppResource(Enum):
    CATEGORY = "category"
    TAG = "tag"


class ResourceDeletedMessage(BaseModel):
    message: Optional[str] = "Resource deleted successfully."
    public_id: str
    resource: AppResource
