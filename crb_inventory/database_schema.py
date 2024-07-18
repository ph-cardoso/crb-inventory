from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TEXT, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, registry

mapper_registry = registry()


# category table
@mapper_registry.mapped_as_dataclass
class Category:
    __tablename__ = "category"
    id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=False),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        TEXT, unique=True, index=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, init=False, server_default="true"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# tag table
@mapper_registry.mapped_as_dataclass
class Tag:
    __tablename__ = "tag"
    id: Mapped[str] = mapped_column(PG_UUID(as_uuid=False), primary_key=True)
    name: Mapped[str] = mapped_column(
        TEXT, unique=True, index=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, init=False, server_default="true"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# custom_fields table
@mapper_registry.mapped_as_dataclass
class CustomField:
    __tablename__ = "custom_field"
    id: Mapped[str] = mapped_column(PG_UUID(as_uuid=False), primary_key=True)
    name: Mapped[str] = mapped_column(
        TEXT, unique=True, index=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, init=False, server_default="true"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# item table
@mapper_registry.mapped_as_dataclass
class Item:
    __tablename__ = "item"
    id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=False),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        TEXT, unique=True, index=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, init=False, server_default="true"
    )
    category_id: Mapped[str] = mapped_column(
        ForeignKey("category.id"), nullable=False
    )
    minimum_threshold: Mapped[int] = mapped_column(INTEGER, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(INTEGER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
