from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_session
from ...models.custom_field import (
    CustomFieldCreateRequest,
    CustomFieldListResponse,
    CustomFieldResponse,
    CustomFieldUpdateRequest,
)
from ...models.utils import ResourceDeletedMessage
from ...services.custom_field import (
    create_custom_field,
    delete_custom_field,
    read_custom_field,
    read_custom_fields,
    update_custom_field,
)

router = APIRouter(prefix="/custom_field", tags=["custom_field"])


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=CustomFieldListResponse,
    summary="Get custom_field list",
)
async def read_custom_fields_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page"
    ),
    session: Session = Depends(get_session),
) -> CustomFieldListResponse:
    return read_custom_fields(page=page, page_size=page_size, session=session)


@router.get(
    "/{custom_field_id}",
    status_code=HTTPStatus.OK,
    response_model=CustomFieldResponse,
    summary="Get custom_field by ID",
)
async def read_custom_field_endpoint(
    custom_field_id: str,
    session: Session = Depends(get_session),
) -> CustomFieldResponse:
    return read_custom_field(custom_field_id=custom_field_id, session=session)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=CustomFieldResponse,
    summary="Create a custom_field",
)
async def create_custom_field_endpoint(
    body: CustomFieldCreateRequest,
    session: Session = Depends(get_session),
) -> CustomFieldResponse:
    return create_custom_field(body=body, session=session)


@router.put(
    "/{custom_field_id}",
    status_code=HTTPStatus.OK,
    response_model=CustomFieldResponse,
    summary="Update a custom_field",
)
async def update_custom_field_endpoint(
    custom_field_id: str,
    body: CustomFieldUpdateRequest,
    session: Session = Depends(get_session),
) -> CustomFieldResponse:
    return update_custom_field(
        custom_field_id=custom_field_id, body=body, session=session
    )


@router.delete(
    "/{custom_field_id}",
    status_code=HTTPStatus.OK,
    response_model=ResourceDeletedMessage,
    summary="Delete a custom_field",
)
async def delete_custom_field_endpoint(
    custom_field_id: str,
    session: Session = Depends(get_session),
) -> ResourceDeletedMessage:
    return delete_custom_field(
        custom_field_id=custom_field_id, session=session
    )
