import re

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Tag
from ..models.exceptions.resource import InvalidId, ResourceNotFound
from ..models.exceptions.tag import InvalidTagName, TagNameAlreadyExists
from ..models.tag import (
    TagCreateRequest,
    TagListResponse,
    TagResponse,
)
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.utils import validate_uuid


def read_tags(
    page: int,
    page_size: int,
    session: Session,
) -> TagListResponse:
    offset = (page - 1) * page_size
    where_clause = Tag.is_active.is_(True)

    tags_query = (
        select(
            Tag.public_id,
            Tag.name,
            Tag.description,
            Tag.is_active,
            Tag.created_at,
            Tag.updated_at,
        )
        .where(where_clause)
        .offset(offset)
        .limit(page_size)
        .order_by(Tag.id.desc())
    )

    total_count_query = select(func.count(Tag.id)).where(where_clause)

    total_count = session.scalar(total_count_query)
    tags = session.execute(tags_query)

    return TagListResponse(
        result=tags,
        total=total_count,
        page=page,
        page_size=page_size,
    )


def read_tag(
    tag_id: str,
    session: Session,
) -> TagResponse:
    if not validate_uuid(tag_id):
        raise InvalidId(value=tag_id)  # pragma: no cover

    tag_query = select(Tag).where(Tag.public_id == tag_id)
    tag = session.scalar(tag_query)

    if not tag:
        raise ResourceNotFound(resource=AppResource.TAG)  # pragma: no cover

    return TagResponse(result=tag)


def create_tag(
    body: TagCreateRequest,
    session: Session,
) -> TagResponse:
    tag_query_by_name = select(Tag).where(Tag.name == body.name)
    tag_by_name = session.scalar(tag_query_by_name)

    if tag_by_name:
        raise TagNameAlreadyExists()  # pragma: no cover

    validate_tag_name(body.name)

    tag = Tag(
        name=body.name,
        description=body.description,
    )

    session.add(tag)
    session.commit()
    session.refresh(tag)

    return TagResponse(result=tag)


def update_tag(
    tag_id: str,
    body: TagCreateRequest,
    session: Session,
) -> TagResponse:
    if not validate_uuid(tag_id):
        raise InvalidId(value=tag_id)  # pragma: no cover

    tag_query = select(Tag).where(Tag.public_id == tag_id)
    tag = session.scalar(tag_query)

    if not tag:
        raise ResourceNotFound(resource=AppResource.TAG)  # pragma: no cover

    validate_tag_name(body.name)

    tag_query_by_name = select(Tag).where(
        Tag.name == body.name and Tag.public_id != tag_id
    )
    tag_by_name = session.scalar(tag_query_by_name)

    if tag_by_name:
        raise TagNameAlreadyExists()  # pragma: no cover

    tag.name = body.name
    tag.description = body.description
    tag.is_active = body.is_active

    session.commit()
    session.refresh(tag)

    return TagResponse(result=tag)


def delete_tag(
    tag_id: str,
    session: Session,
) -> ResourceDeletedMessage:
    if not validate_uuid(tag_id):
        raise InvalidId(value=tag_id)  # pragma: no cover

    tag_query = select(Tag).where(Tag.public_id == tag_id)
    tag = session.scalar(tag_query)

    if not tag:
        raise ResourceNotFound(resource=AppResource.TAG)  # pragma: no cover

    session.delete(tag)
    session.commit()

    return ResourceDeletedMessage(
        public_id=tag.public_id, resource=AppResource.TAG
    )


def validate_tag_name(name: str) -> None:
    max_tag_length = 50
    regex = r"^[a-z0-9]+(-[a-z0-9]+)*$"

    if len(name) > max_tag_length:
        raise InvalidTagName(value=name)  # pragma: no cover

    if not re.match(regex, name):
        raise InvalidTagName(value=name)  # pragma: no cover
