from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Category
from ..models.category import (
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryResponse,
)
from ..models.exceptions.category import CategoryNameAlreadyExists
from ..models.exceptions.resource import InvalidId, ResourceNotFound
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.utils import validate_uuid


def read_categories(
    page: int,
    page_size: int,
    session: Session,
) -> CategoryListResponse:
    offset = (page - 1) * page_size
    where_clause = Category.is_active.is_(True)

    categories_query = (
        select(
            Category.public_id,
            Category.name,
            Category.description,
            Category.is_active,
            Category.created_at,
            Category.updated_at,
        )
        .where(where_clause)
        .offset(offset)
        .limit(page_size)
        .order_by(Category.id.desc())
    )

    total_count_query = select(func.count(Category.id)).where(where_clause)

    total_count = session.scalar(total_count_query)
    categories = session.execute(categories_query)

    return CategoryListResponse(
        result=categories,
        total=total_count,
        page=page,
        page_size=page_size,
    )


def read_category(
    category_id: str,
    session: Session,
) -> CategoryResponse:
    if not validate_uuid(category_id):
        raise InvalidId(value=category_id)  # pragma: no cover

    category_query = select(Category).where(Category.public_id == category_id)
    category = session.scalar(category_query)

    if not category:
        raise ResourceNotFound(
            resource=AppResource.CATEGORY
        )  # pragma: no cover

    return CategoryResponse(result=category)


def create_category(
    body: CategoryCreateRequest,
    session: Session,
) -> CategoryResponse:
    category_query_by_name = select(Category).where(Category.name == body.name)
    category_by_name = session.scalar(category_query_by_name)

    if category_by_name:
        raise CategoryNameAlreadyExists()  # pragma: no cover

    category = Category(
        name=body.name,
        description=body.description,
    )

    session.add(category)
    session.commit()
    session.refresh(category)

    return CategoryResponse(result=category)


def update_category(
    category_id: str,
    body: CategoryCreateRequest,
    session: Session,
) -> CategoryResponse:
    if not validate_uuid(category_id):
        raise InvalidId(value=category_id)  # pragma: no cover

    category_query = select(Category).where(Category.public_id == category_id)
    category = session.scalar(category_query)

    if not category:
        raise ResourceNotFound(
            resource=AppResource.CATEGORY
        )  # pragma: no cover

    category_query_by_name = select(Category).where(
        Category.name == body.name and Category.public_id != category_id
    )
    category_by_name = session.scalar(category_query_by_name)

    if category_by_name:
        raise CategoryNameAlreadyExists()  # pragma: no cover

    category.name = body.name
    category.description = body.description
    category.is_active = body.is_active

    session.commit()
    session.refresh(category)

    return CategoryResponse(result=category)


def delete_category(
    category_id: str,
    session: Session,
) -> ResourceDeletedMessage:
    if not validate_uuid(category_id):
        raise InvalidId(value=category_id)  # pragma: no cover

    category_query = select(Category).where(Category.public_id == category_id)
    category = session.scalar(category_query)

    if not category:
        raise ResourceNotFound(
            resource=AppResource.CATEGORY
        )  # pragma: no cover

    session.delete(category)
    session.commit()

    return ResourceDeletedMessage(
        public_id=category.public_id, resource=AppResource.CATEGORY
    )
