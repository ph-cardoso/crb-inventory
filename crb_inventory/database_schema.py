from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TEXT, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

mapper_registry = registry()

# Tabelas intermediárias
item_tag_association = Table(
    "item_tag_association",
    mapper_registry.metadata,
    Column(
        "item_id",
        PG_UUID(as_uuid=False),
        ForeignKey("item.id"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        PG_UUID(as_uuid=False),
        ForeignKey("tag.id"),
        primary_key=True,
    ),
)


# category table
@mapper_registry.mapped_as_dataclass
class Category:
    __tablename__ = "category"
    id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=False),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(TEXT, unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, init=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    items: Mapped[List["Item"]] = relationship("Item", backref="category", init=False)


# tag table
@mapper_registry.mapped_as_dataclass
class Tag:
    __tablename__ = "tag"
    id: Mapped[str] = mapped_column(PG_UUID(as_uuid=False), primary_key=True)
    name: Mapped[str] = mapped_column(TEXT, unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, init=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    items: Mapped[List["Item"]] = relationship(
        secondary=item_tag_association, back_populates="tags", init=False
    )


# item table
@mapper_registry.mapped_as_dataclass
class Item:
    __tablename__ = "item"
    id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=False),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(TEXT, unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, init=False, server_default="true")
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"), nullable=False)
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
    tags: Mapped[List["Tag"]] = relationship(
        secondary=item_tag_association, back_populates="items", init=False
    )
