from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from pydantic import AfterValidator
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from ...core.database import get_session
from ...models.item import (
    ItemCreateRequest,
    ItemListResponse,
    ItemPatchRequest,
    ItemResponse,
    ItemTagAddMessage,
    ItemTagDeleteMessage,
    ItemTagListResponse,
    ItemUpdateRequest,
)
from ...models.utils import ResourceDeletedMessage
from ...models.validators import validate_uuid_value
from ...services.item import (
    add_tag_to_item,
    create_item,
    delete_item,
    delete_tag_from_item,
    patch_item,
    read_item,
    read_item_tags,
    read_items,
    read_items_by_category,
    read_items_by_tag,
    update_item,
)

router = APIRouter(prefix="/item", tags=["item"])


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=ItemListResponse,
    summary="Get item list",
)
async def read_items_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    session: Session = Depends(get_session),
) -> ItemListResponse:
    return read_items(page=page, page_size=page_size, session=session)


@router.get(
    "/{item_id}",
    status_code=HTTPStatus.OK,
    response_model=ItemResponse,
    summary="Get item by ID",
)
async def read_item_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ItemResponse:
    return read_item(item_id=item_id, session=session)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=ItemResponse,
    summary="Create an item",
)
async def create_item_endpoint(
    body: ItemCreateRequest,
    session: Session = Depends(get_session),
) -> ItemResponse:
    return create_item(body=body, session=session)


@router.put(
    "/{item_id}",
    status_code=HTTPStatus.OK,
    response_model=ItemResponse,
    summary="Update an item",
)
async def update_item_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    body: ItemUpdateRequest,
    session: Session = Depends(get_session),
) -> ItemResponse:
    return update_item(item_id=item_id, body=body, session=session)


@router.delete(
    "/{item_id}",
    status_code=HTTPStatus.OK,
    response_model=ResourceDeletedMessage,
    summary="Delete an item",
)
async def delete_item_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ResourceDeletedMessage:
    return delete_item(item_id=item_id, session=session)


@router.patch(
    "/{item_id}",
    status_code=HTTPStatus.OK,
    response_model=ItemResponse,
    summary="Patch one or more parameters of an item",
)
async def patch_item_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    body: ItemPatchRequest,
    session: Session = Depends(get_session),
) -> ItemResponse:
    return patch_item(
        item_id=item_id,
        body=body,
        session=session,
    )


@router.get(
    "/{item_id}/tag",
    status_code=HTTPStatus.OK,
    response_model=ItemTagListResponse,
    summary="Get tags of an item",
)
async def read_item_tags_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ItemTagListResponse:
    return read_item_tags(item_id=item_id, session=session)


@router.post(
    "/{item_id}/tag/{tag_id}",
    status_code=HTTPStatus.CREATED,
    response_model=ItemTagAddMessage,
    summary="Add a tag to an item",
)
async def add_tag_to_item_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ItemTagAddMessage:
    return add_tag_to_item(item_id=item_id, tag_id=tag_id, session=session)


@router.delete(
    "/{item_id}/tag/{tag_id}",
    status_code=HTTPStatus.OK,
    response_model=ItemTagDeleteMessage,
    summary="Delete a tag from an item",
)
async def delete_tag_from_item_endpoint(
    item_id: Annotated[str, AfterValidator(validate_uuid_value)],
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ItemTagDeleteMessage:
    return delete_tag_from_item(item_id=item_id, tag_id=tag_id, session=session)


@router.get(
    "/category/{category_id}",
    status_code=HTTPStatus.OK,
    response_model=ItemListResponse,
    summary="Get item list by category",
)
async def read_items_by_category_endpoint(
    category_id: Annotated[str, AfterValidator(validate_uuid_value)],
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    session: Session = Depends(get_session),
) -> ItemListResponse:
    return read_items_by_category(
        page=page, page_size=page_size, category_id=category_id, session=session
    )


@router.get(
    "/tag/{tag_id}",
    status_code=HTTPStatus.OK,
    response_model=ItemListResponse,
    summary="Get item list by tag",
)
async def read_items_by_tag_endpoint(
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    session: Session = Depends(get_session),
) -> ItemListResponse:
    return read_items_by_tag(
        page=page, page_size=page_size, tag_id=tag_id, session=session
    )
