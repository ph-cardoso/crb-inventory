from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Category
from ..models.category import (
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryPublic,
    CategoryResponse,
)
from ..models.exceptions.resource_utils import InvalidId, ResourceNotFound
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

    categories_result = [
        CategoryPublic(
            public_id=category.public_id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
        for category in categories
    ]

    return CategoryListResponse(
        result=categories_result,
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

    category_result = CategoryPublic(
        public_id=category.public_id,
        name=category.name,
        description=category.description,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )

    return CategoryResponse(result=category_result)


def create_category(
    body: CategoryCreateRequest,
    session: Session,
) -> CategoryResponse:
    category = Category(
        name=body.name,
        description=body.description,
    )

    category_exists = (
        session.query(Category).filter(Category.name == category.name).first()
    )

    if category_exists:
        raise ValueError("Category name already exists")  # pragma: no cover

    session.add(category)
    session.commit()
    session.refresh(category)

    category_result = CategoryPublic(
        public_id=category.public_id,
        name=category.name,
        description=category.description,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )
    return CategoryResponse(result=category_result)


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

    category.name = body.name
    category.description = body.description
    category.is_active = body.is_active

    session.commit()
    session.refresh(category)

    category_result = CategoryPublic(
        public_id=category.public_id,
        name=category.name,
        description=category.description,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )

    return CategoryResponse(result=category_result)


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
