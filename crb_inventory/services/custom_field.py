import re

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import CustomField
from ..models.custom_field import (
    CustomFieldCreateRequest,
    CustomFieldListResponse,
    CustomFieldResponse,
)
from ..models.exceptions.custom_field import (
    CustomFieldNameAlreadyExists,
    InvalidCustomFieldName,
)
from ..models.exceptions.resource import InvalidId, ResourceNotFound
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.uuid import generate_uuid_v7, validate_uuid


def read_custom_fields(
    page: int,
    page_size: int,
    session: Session,
) -> CustomFieldListResponse:
    offset = (page - 1) * page_size
    where_clause = CustomField.is_active.is_(True)

    custom_fields_query = (
        select(
            CustomField.id,
            CustomField.name,
            CustomField.description,
            CustomField.is_active,
            CustomField.created_at,
            CustomField.updated_at,
        )
        .where(where_clause)
        .offset(offset)
        .limit(page_size)
        .order_by(CustomField.id.desc())
    )

    total_count_query = select(func.count(CustomField.id)).where(where_clause)

    total_count = session.scalar(total_count_query)
    custom_fields = session.execute(custom_fields_query)

    return CustomFieldListResponse(
        result=custom_fields,
        total=total_count,
        page=page,
        page_size=page_size,
    )


def read_custom_field(
    custom_field_id: str,
    session: Session,
) -> CustomFieldResponse:
    if not validate_uuid(custom_field_id):
        raise InvalidId(value=custom_field_id)  # pragma: no cover

    custom_field_query = select(CustomField).where(
        CustomField.id == custom_field_id
    )
    custom_field = session.scalar(custom_field_query)

    if not custom_field:
        raise ResourceNotFound(
            resource=AppResource.CUSTOM_FIELD
        )  # pragma: no cover

    return CustomFieldResponse(result=custom_field)


def create_custom_field(
    body: CustomFieldCreateRequest,
    session: Session,
) -> CustomFieldResponse:
    custom_field_query_by_name = select(CustomField).where(
        CustomField.name == body.name
    )
    custom_field_by_name = session.scalar(custom_field_query_by_name)

    if custom_field_by_name:
        raise CustomFieldNameAlreadyExists()  # pragma: no cover

    validate_custom_field_name(body.name)

    custom_field = CustomField(
        id=generate_uuid_v7(),
        name=body.name,
        description=body.description,
    )

    session.add(custom_field)
    session.commit()
    session.refresh(custom_field)

    return CustomFieldResponse(result=custom_field)


def update_custom_field(
    custom_field_id: str,
    body: CustomFieldCreateRequest,
    session: Session,
) -> CustomFieldResponse:
    if not validate_uuid(custom_field_id):
        raise InvalidId(value=custom_field_id)  # pragma: no cover

    custom_field_query = select(CustomField).where(
        CustomField.id == custom_field_id
    )
    custom_field = session.scalar(custom_field_query)

    if not custom_field:
        raise ResourceNotFound(
            resource=AppResource.CUSTOM_FIELD
        )  # pragma: no cover

    validate_custom_field_name(body.name)

    custom_field_query_by_name = select(CustomField).where(
        CustomField.name == body.name and CustomField.id != custom_field_id
    )
    custom_field_by_name = session.scalar(custom_field_query_by_name)

    if custom_field_by_name:
        raise CustomFieldNameAlreadyExists()  # pragma: no cover

    custom_field.name = body.name
    custom_field.description = body.description
    custom_field.is_active = body.is_active

    session.commit()
    session.refresh(custom_field)

    return CustomFieldResponse(result=custom_field)


def delete_custom_field(
    custom_field_id: str,
    session: Session,
) -> ResourceDeletedMessage:
    if not validate_uuid(custom_field_id):
        raise InvalidId(value=custom_field_id)  # pragma: no cover

    custom_field_query = select(CustomField).where(
        CustomField.id == custom_field_id
    )
    custom_field = session.scalar(custom_field_query)

    if not custom_field:
        raise ResourceNotFound(
            resource=AppResource.CUSTOM_FIELD
        )  # pragma: no cover

    session.delete(custom_field)
    session.commit()

    return ResourceDeletedMessage(
        id=custom_field.id, resource=AppResource.CUSTOM_FIELD
    )


def validate_custom_field_name(name: str) -> None:
    max_custom_field_length = 30
    regex = r"^[a-z0-9]+(_[a-z0-9]+)*$"

    if len(name) > max_custom_field_length:
        raise InvalidCustomFieldName(value=name)  # pragma: no cover

    if not re.match(regex, name):
        raise InvalidCustomFieldName(value=name)  # pragma: no cover
