from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from pydantic import AfterValidator
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from ...core.database import get_session
from ...models.category import (
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryPatchRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from ...models.utils import ResourceDeletedMessage
from ...models.validators import validate_uuid_value
from ...services.category import (
    create_category,
    delete_category,
    patch_category,
    read_categories,
    read_category,
    update_category,
)

router = APIRouter(prefix="/category", tags=["category"])


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=CategoryListResponse,
    summary="Get category list",
)
async def read_categories_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    session: Session = Depends(get_session),
) -> CategoryListResponse:
    return read_categories(page=page, page_size=page_size, session=session)


@router.get(
    "/{category_id}",
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
    summary="Get category by ID",
)
async def read_category_endpoint(
    category_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> CategoryResponse:
    return read_category(category_id=category_id, session=session)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=CategoryResponse,
    summary="Create a category",
)
async def create_category_endpoint(
    body: CategoryCreateRequest,
    session: Session = Depends(get_session),
) -> CategoryResponse:
    return create_category(body=body, session=session)


@router.put(
    "/{category_id}",
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
    summary="Update a category",
)
async def update_category_endpoint(
    category_id: Annotated[str, AfterValidator(validate_uuid_value)],
    body: CategoryUpdateRequest,
    session: Session = Depends(get_session),
) -> CategoryResponse:
    return update_category(category_id=category_id, body=body, session=session)


@router.delete(
    "/{category_id}",
    status_code=HTTPStatus.OK,
    response_model=ResourceDeletedMessage,
    summary="Delete a category",
)
async def delete_category_endpoint(
    category_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ResourceDeletedMessage:
    return delete_category(category_id=category_id, session=session)


@router.patch(
    "/{category_id}",
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
    summary="Patch one or more parameters of a category",
)
async def patch_category_endpoint(
    category_id: Annotated[str, AfterValidator(validate_uuid_value)],
    body: CategoryPatchRequest,
    session: Session = Depends(get_session),
) -> CategoryResponse:
    return patch_category(
        category_id=category_id,
        body=body,
        session=session,
    )
