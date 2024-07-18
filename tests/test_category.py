from http import HTTPStatus

from crb_inventory.models.exceptions.category import CategoryNameAlreadyExists
from crb_inventory.models.exceptions.resource import (
    ResourceNotFound,
)
from crb_inventory.models.utils import AppResource
from tests.factories import CategoryFactory


def test_read_categories_should_return_6(session, client):
    route = "/v1/category/"
    expected_categories = 6
    expected_default_page = 1
    expected_default_page_size = 10

    session.bulk_save_objects(
        CategoryFactory.create_batch(expected_categories)
    )
    session.commit()

    response = client.get(route)

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_categories
    assert response.json()["total"] == expected_categories

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_default_page
    assert response.json()["page_size"] == expected_default_page_size


def test_read_categories_should_return_5_in_page_2(session, client):
    route = "/v1/category/"
    expected_categories = 25
    expected_categories_in_page_2 = 5
    expected_page = 2
    expected_page_size = 20

    session.bulk_save_objects(
        CategoryFactory.create_batch(expected_categories)
    )
    session.commit()

    response = client.get(
        f"{route}?page={expected_page}&page_size={expected_page_size}"
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_categories_in_page_2
    assert response.json()["total"] == expected_categories

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_page
    assert response.json()["page_size"] == expected_page_size


def test_create_category_should_return_201_and_generated_data(client):
    route = "/v1/category/"
    category_data = {
        "name": "Category 1",
        "description": "Category 1 description",
    }

    response = client.post(route, json=category_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["result"]["name"] == category_data["name"]
    assert (
        response.json()["result"]["description"]
        == category_data["description"]
    )
    assert response.json()["result"]["is_active"] is True
    assert "id" in response.json()["result"]
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_read_category_should_return_200_and_generated_data(session, client):
    route = "/v1/category/"
    category = CategoryFactory()
    session.add(category)
    session.commit()

    response = client.get(f"{route}{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == category.name
    assert response.json()["result"]["description"] == category.description
    assert response.json()["result"]["is_active"] == category.is_active
    assert response.json()["result"]["id"] == category.id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_update_category_should_return_200_and_updated_data(session, client):
    route = "/v1/category/"
    category = CategoryFactory()
    session.add(category)
    session.commit()

    category_data = {
        "name": "Category 1 updated",
        "description": "Category 1 description updated",
        "is_active": False,
    }

    response = client.put(f"{route}{category.id}", json=category_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == category_data["name"]
    assert (
        response.json()["result"]["description"]
        == category_data["description"]
    )
    assert response.json()["result"]["is_active"] == category_data["is_active"]
    assert response.json()["result"]["id"] == category.id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]
    assert (
        response.json()["result"]["updated_at"]
        != response.json()["result"]["created_at"]
    )


def test_delete_category_should_return_200_and_deleted_message(
    session, client
):
    route = "/v1/category/"
    category = CategoryFactory()
    session.add(category)
    session.commit()

    response = client.delete(f"{route}{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Resource deleted successfully."
    assert response.json()["id"] == category.id
    assert response.json()["resource"] == AppResource.CATEGORY.value


def test_category_not_found_exception_should_return_404(client):
    route = "/v1/category/"
    random_id = "56f0572c-1dec-4b4d-b517-4cac967146a7"
    response = client.get(f"{route}{random_id}")

    exception = ResourceNotFound(resource=AppResource.CATEGORY)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == f"{route}{random_id}"


def test_invalid_id_exception_should_return_422(client):
    route = "/v1/category/"
    invalid_input = "invalid-id"
    response = client.get(f"{route}{invalid_input}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["input"] == invalid_input
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, value should be a valid UUID"
    )


def test_category_name_already_exists_exception_should_return_422(
    session, client
):
    route = "/v1/category/"
    category = CategoryFactory()
    session.add(category)
    session.commit()

    category_data = {
        "name": category.name,
    }

    response = client.post(route, json=category_data)

    exception = CategoryNameAlreadyExists()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == route
