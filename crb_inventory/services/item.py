from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Category, Item
from ..models.exceptions.item import ItemNameAlreadyExists
from ..models.exceptions.resource import ResourceNotFound
from ..models.item import (
    ItemCreateRequest,
    ItemListResponse,
    ItemResponse,
    ItemUpdateRequest,
)
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.uuid import generate_uuid_v7


def read_items(
    page: int,
    page_size: int,
    session: Session,
) -> ItemListResponse:
    offset = (page - 1) * page_size
    where_clause = Item.is_active.is_(True)

    items_query = (
        select(
            Item.id,
            Item.name,
            Item.description,
            Item.is_active,
            Item.category_id,
            Item.minimum_threshold,
            Item.stock_quantity,
            Item.created_at,
            Item.updated_at,
        )
        .where(where_clause)
        .offset(offset)
        .limit(page_size)
        .order_by(Item.id.desc())
    )

    total_count_query = select(func.count(Item.id)).where(where_clause)

    total_count = session.scalar(total_count_query)
    items = session.execute(items_query).all()

    return ItemListResponse(
        result=items,
        total=total_count,
        page=page,
        page_size=page_size,
    )


def read_item(
    item_id: str,
    session: Session,
) -> ItemResponse:
    item_query = select(Item).where(Item.id == item_id)
    item = session.scalar(item_query)

    if not item:
        raise ResourceNotFound(resource=AppResource.ITEM)  # pragma: no cover

    return ItemResponse(result=item)


def create_item(
    body: ItemCreateRequest,
    session: Session,
) -> ItemResponse:
    item_query_by_name = select(Item).where(Item.name == body.name)
    item_by_name = session.scalar(item_query_by_name)

    if item_by_name:
        raise ItemNameAlreadyExists()  # pragma: no cover

    # Check if category_id exists
    category_query = select(Category).where(Category.id == body.category_id)
    category = session.scalar(category_query)

    if not category:
        raise ResourceNotFound(
            resource=AppResource.CATEGORY
        )  # pragma: no cover

    if not body.minimum_threshold:
        body.minimum_threshold = 0

    if not body.stock_quantity:
        body.stock_quantity = 0

    item = Item(
        id=generate_uuid_v7(),
        name=body.name,
        description=body.description,
        category_id=body.category_id,
        minimum_threshold=body.minimum_threshold,
        stock_quantity=body.stock_quantity,
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    print(item)

    return ItemResponse(result=item)


def update_item(
    item_id: str,
    body: ItemUpdateRequest,
    session: Session,
) -> ItemResponse:
    item_query = select(Item).where(Item.id == item_id)
    item = session.scalar(item_query)

    if not item:
        raise ResourceNotFound(resource=AppResource.ITEM)  # pragma: no cover

    item_query_by_name = select(Item).where(
        Item.name == body.name and Item.id != item_id
    )
    item_by_name = session.scalar(item_query_by_name)

    if item_by_name:
        raise ItemNameAlreadyExists()  # pragma: no cover

    item.name = body.name
    item.description = body.description
    item.is_active = body.is_active
    item.category_id = body.category_id
    item.minimum_threshold = body.minimum_threshold
    item.stock_quantity = body.stock_quantity

    session.commit()
    session.refresh(item)

    return ItemResponse(result=item)


def delete_item(
    item_id: str,
    session: Session,
) -> ResourceDeletedMessage:
    item_query = select(Item).where(Item.id == item_id)
    item = session.scalar(item_query)

    if not item:
        raise ResourceNotFound(resource=AppResource.ITEM)  # pragma: no cover

    session.delete(item)
    session.commit()

    return ResourceDeletedMessage(id=item.id, resource=AppResource.ITEM)
