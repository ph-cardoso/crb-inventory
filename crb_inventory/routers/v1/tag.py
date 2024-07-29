from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from pydantic import AfterValidator
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from ...core.database import get_session
from ...models.tag import (
    TagCreateRequest,
    TagListResponse,
    TagPatchRequest,
    TagResponse,
    TagUpdateRequest,
)
from ...models.utils import ResourceDeletedMessage
from ...models.validators import validate_uuid_value
from ...services.tag import (
    create_tag,
    delete_tag,
    patch_tag,
    read_tag,
    read_tags,
    update_tag,
)

router = APIRouter(prefix="/tag", tags=["tag"])


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=TagListResponse,
    summary="Get tag list",
)
async def read_tags_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    session: Session = Depends(get_session),
) -> TagListResponse:
    return read_tags(page=page, page_size=page_size, session=session)


@router.get(
    "/{tag_id}",
    status_code=HTTPStatus.OK,
    response_model=TagResponse,
    summary="Get tag by ID",
)
async def read_tag_endpoint(
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> TagResponse:
    return read_tag(tag_id=tag_id, session=session)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=TagResponse,
    summary="Create a tag",
)
async def create_tag_endpoint(
    body: TagCreateRequest,
    session: Session = Depends(get_session),
) -> TagResponse:
    return create_tag(body=body, session=session)


@router.put(
    "/{tag_id}",
    status_code=HTTPStatus.OK,
    response_model=TagResponse,
    summary="Update a tag",
)
async def update_tag_endpoint(
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    body: TagUpdateRequest,
    session: Session = Depends(get_session),
) -> TagResponse:
    return update_tag(tag_id=tag_id, body=body, session=session)


@router.delete(
    "/{tag_id}",
    status_code=HTTPStatus.OK,
    response_model=ResourceDeletedMessage,
    summary="Delete a tag",
)
async def delete_tag_endpoint(
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    session: Session = Depends(get_session),
) -> ResourceDeletedMessage:
    return delete_tag(tag_id=tag_id, session=session)


@router.patch(
    "/{tag_id}",
    status_code=HTTPStatus.OK,
    response_model=TagResponse,
    summary="Patch one or more parameters of a tag",
)
async def patch_tag_endpoint(
    tag_id: Annotated[str, AfterValidator(validate_uuid_value)],
    body: TagPatchRequest,
    session: Session = Depends(get_session),
) -> TagResponse:
    return patch_tag(tag_id=tag_id, body=body, session=session)
