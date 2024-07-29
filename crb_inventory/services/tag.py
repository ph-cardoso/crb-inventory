from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Tag
from ..models.exceptions.resource import ResourceNotFound
from ..models.exceptions.tag import TagNameAlreadyExists
from ..models.tag import (
    TagCreateRequest,
    TagListResponse,
    TagPatchRequest,
    TagResponse,
    TagUpdateRequest,
)
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.uuid import generate_uuid_v7


def read_tags(
    page: int,
    page_size: int,
    session: Session,
) -> TagListResponse:
    offset = (page - 1) * page_size
    where_clause = Tag.is_active.is_(True)

    tags_query = (
        select(
            Tag.id,
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
    tag = check_tag_exists(tag_id, session)

    return TagResponse(result=tag)


def create_tag(
    body: TagCreateRequest,
    session: Session,
) -> TagResponse:
    check_tag_name_exists(body.name, session)

    tag = Tag(
        id=generate_uuid_v7(),
        name=body.name,
        description=body.description,
    )

    session.add(tag)
    session.commit()
    session.refresh(tag)

    return TagResponse(result=tag)


def update_tag(
    tag_id: str,
    body: TagUpdateRequest,
    session: Session,
) -> TagResponse:
    tag = check_tag_exists(tag_id, session)

    check_tag_name_exists(body.name, session, previous_tag_id=tag_id)

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
    tag = check_tag_exists(tag_id, session)

    session.delete(tag)
    session.commit()

    return ResourceDeletedMessage(id=tag.id, resource=AppResource.TAG)


def patch_tag(
    tag_id: str,
    body: TagPatchRequest,
    session: Session,
) -> TagResponse:
    tag = check_tag_exists(tag_id, session)

    if body.name is not None:
        check_tag_name_exists(body.name, session, previous_tag_id=tag_id)
        tag.name = body.name

    if body.description is not None:
        tag.description = body.description

    if body.is_active is not None:
        tag.is_active = body.is_active

    session.commit()
    session.refresh(tag)

    return TagResponse(result=tag)


def check_tag_name_exists(
    name: str,
    session: Session,
    previous_tag_id: str = None,
):
    tag_query = select(Tag).where(Tag.name == name)
    tag = session.scalar(tag_query)

    if tag:
        if previous_tag_id and tag.id == previous_tag_id:
            return

        raise TagNameAlreadyExists()


def check_tag_exists(
    tag_id: str,
    session: Session,
) -> Tag:
    tag_query = select(Tag).where(Tag.id == tag_id)
    tag = session.scalar(tag_query)

    if not tag:
        raise ResourceNotFound(resource=AppResource.TAG)

    return tag
