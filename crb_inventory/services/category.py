from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database_schema import Category
from ..models.category import (
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryPatchRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from ..models.exceptions.category import CategoryNameAlreadyExists
from ..models.exceptions.resource import ResourceNotFound
from ..models.utils import AppResource, ResourceDeletedMessage
from ..services.uuid import generate_uuid_v7


def read_categories(
    page: int,
    page_size: int,
    session: Session,
) -> CategoryListResponse:
    offset = (page - 1) * page_size
    where_clause = Category.is_active.is_(True)

    categories_query = (
        select(
            Category.id,
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
    categories = session.execute(categories_query).all()

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
    category = check_category_exists(category_id=category_id, session=session)

    return CategoryResponse(result=category)


def create_category(
    body: CategoryCreateRequest,
    session: Session,
) -> CategoryResponse:
    check_category_name_exists(name=body.name, session=session)

    category = Category(
        id=generate_uuid_v7(),
        name=body.name,
        description=body.description,
    )

    session.add(category)
    session.commit()
    session.refresh(category)

    return CategoryResponse(result=category)


def update_category(
    category_id: str,
    body: CategoryUpdateRequest,
    session: Session,
) -> CategoryResponse:
    category = check_category_exists(category_id=category_id, session=session)

    check_category_name_exists(
        name=body.name, session=session, previous_category_id=category_id
    )

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
    category = check_category_exists(category_id=category_id, session=session)

    session.delete(category)
    session.commit()

    return ResourceDeletedMessage(id=category.id, resource=AppResource.CATEGORY)


def patch_category(
    category_id: str,
    body: CategoryPatchRequest,
    session: Session,
) -> CategoryResponse:
    category = check_category_exists(category_id=category_id, session=session)

    if body.name is not None:
        check_category_name_exists(
            name=body.name, session=session, previous_category_id=category_id
        )
        category.name = body.name

    if body.description is not None:
        category.description = body.description

    if body.is_active is not None:
        category.is_active = body.is_active

    session.commit()
    session.refresh(category)

    return CategoryResponse(result=category)


def check_category_name_exists(
    name: str,
    session: Session,
    previous_category_id: str = None,
):
    category_query = select(Category).where(Category.name == name)
    category = session.scalar(category_query)

    if category:
        if previous_category_id and category.id == previous_category_id:
            return

        raise CategoryNameAlreadyExists()


def check_category_exists(
    category_id: str,
    session: Session,
) -> Category:
    category_query = select(Category).where(Category.id == category_id)
    category = session.scalar(category_query)

    if not category:
        raise ResourceNotFound(resource=AppResource.CATEGORY)

    return category
