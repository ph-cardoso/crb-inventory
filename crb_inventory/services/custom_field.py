from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import CustomField
from ..models.custom_field import (
    CustomFieldCreateRequest,
    CustomFieldListResponse,
    CustomFieldPatchRequest,
    CustomFieldResponse,
    CustomFieldUpdateRequest,
)
from ..models.exceptions.custom_field import CustomFieldNameAlreadyExists
from ..models.exceptions.resource import ResourceNotFound
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.uuid import generate_uuid_v7


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
    custom_field = check_custom_field_exists(custom_field_id, session)

    return CustomFieldResponse(result=custom_field)


def create_custom_field(
    body: CustomFieldCreateRequest,
    session: Session,
) -> CustomFieldResponse:
    check_custom_field_name_exists(body.name, session)

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
    body: CustomFieldUpdateRequest,
    session: Session,
) -> CustomFieldResponse:
    custom_field = check_custom_field_exists(custom_field_id, session)

    check_custom_field_name_exists(body.name, session)

    custom_field.name = body.name
    custom_field.description = body.description
    custom_field.is_active = body.is_active

    session.commit()
    session.refresh(custom_field)

    return CustomFieldResponse(result=custom_field)


def patch_custom_field(
    custom_field_id: str,
    body: CustomFieldPatchRequest,
    session: Session,
) -> CustomFieldResponse:
    custom_field = check_custom_field_exists(custom_field_id, session)

    if body.name is not None:
        check_custom_field_name_exists(body.name, session, custom_field_id)
        custom_field.name = body.name

    if body.description is not None:
        custom_field.description = body.description

    if body.is_active is not None:
        custom_field.is_active = body.is_active

    session.commit()
    session.refresh(custom_field)

    return CustomFieldResponse(result=custom_field)


def delete_custom_field(
    custom_field_id: str,
    session: Session,
) -> ResourceDeletedMessage:
    custom_field = check_custom_field_exists(custom_field_id, session)

    session.delete(custom_field)
    session.commit()

    return ResourceDeletedMessage(id=custom_field.id, resource=AppResource.CUSTOM_FIELD)


def check_custom_field_name_exists(
    name: str,
    session: Session,
    previous_custom_field_id: str = None,
):
    custom_field_query = select(CustomField).where(CustomField.name == name)
    custom_field = session.scalar(custom_field_query)

    if custom_field:
        if previous_custom_field_id and custom_field.id == previous_custom_field_id:
            return

        raise CustomFieldNameAlreadyExists()


def check_custom_field_exists(
    custom_field_id: str,
    session: Session,
) -> CustomField:
    custom_field_query = select(CustomField).where(CustomField.id == custom_field_id)
    custom_field = session.scalar(custom_field_query)

    if not custom_field:
        raise ResourceNotFound(resource=AppResource.CUSTOM_FIELD)

    return custom_field
