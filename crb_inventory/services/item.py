from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Item
from ..models.exceptions.item import ItemNameAlreadyExists
from ..models.exceptions.resource import ResourceNotFound
from ..models.item import (
    ItemCreateRequest,
    ItemListResponse,
    ItemPatchRequest,
    ItemResponse,
    ItemUpdateRequest,
)
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.category import check_category_exists
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
    item = check_item_exists(item_id, session)

    return ItemResponse(result=item)


def create_item(
    body: ItemCreateRequest,
    session: Session,
) -> ItemResponse:
    check_item_name_exists(body.name, session)
    check_category_exists(body.category_id, session)

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

    return ItemResponse(result=item)


def update_item(
    item_id: str,
    body: ItemUpdateRequest,
    session: Session,
) -> ItemResponse:
    item = check_item_exists(item_id, session)

    check_item_name_exists(body.name, session, item.id)
    check_category_exists(body.category_id, session)

    for key, value in body.model_dump().items():
        setattr(item, key, value)

    session.commit()
    session.refresh(item)

    return ItemResponse(result=item)


def delete_item(
    item_id: str,
    session: Session,
) -> ResourceDeletedMessage:
    item = check_item_exists(item_id, session)

    session.delete(item)
    session.commit()

    return ResourceDeletedMessage(id=item.id, resource=AppResource.ITEM)


def patch_item(
    item_id: str,
    body: ItemPatchRequest,
    session: Session,
) -> ItemResponse:
    item = check_item_exists(item_id, session)

    if body.name is not None:
        check_item_name_exists(body.name, session, item.id)
        item.name = body.name

    if body.description is not None:
        item.description = body.description

    if body.is_active is not None:
        item.is_active = body.is_active

    if body.category_id is not None:
        check_category_exists(body.category_id, session)
        item.category_id = body.category_id

    if body.minimum_threshold is not None:
        item.minimum_threshold = body.minimum_threshold

    if body.stock_quantity is not None:
        item.stock_quantity = body.stock_quantity

    session.commit()
    session.refresh(item)

    return ItemResponse(result=item)


def check_item_name_exists(
    name: str,
    session: Session,
    previous_item_id: str = None,
):
    item_query = select(Item).where(Item.name == name)
    item = session.scalar(item_query)

    if item:
        if previous_item_id and item.id == previous_item_id:
            return

        raise ItemNameAlreadyExists()


def check_item_exists(
    item_id: str,
    session: Session,
) -> Item:
    item_query = select(Item).where(Item.id == item_id)
    item = session.scalar(item_query)

    if not item:
        raise ResourceNotFound(resource=AppResource.ITEM)

    return item
