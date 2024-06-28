from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, registry

# Use pydantic dataclasses
mapper_registry = registry()


# category table
@mapper_registry.mapped_as_dataclass
class Category:
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    public_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=False),
        init=False,
        unique=True,
        index=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(TEXT, unique=True)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, init=False, server_default="true"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
