from http import HTTPStatus

from crb_inventory.models.exceptions.item import ItemNameAlreadyExists
from crb_inventory.models.exceptions.resource import (
    ResourceNotFound,
)
from crb_inventory.models.utils import AppResource
from tests.factories import CategoryFactory, ItemFactory


def test_read_items_should_return_6(session, client):
    route = "/v1/item/"
    expected_items = 6
    expected_default_page = 1
    expected_default_page_size = 10

    category = CategoryFactory()
    session.add(category)
    session.commit()

    session.bulk_save_objects(
        ItemFactory.create_batch(expected_items, category_id=category.id)
    )
    session.commit()

    response = client.get(route)

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_items
    assert response.json()["total"] == expected_items

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_default_page
    assert response.json()["page_size"] == expected_default_page_size


def test_read_items_should_return_5_in_page_2(session, client):
    route = "/v1/item/"
    expected_items = 25
    expected_items_in_page_2 = 5
    expected_page = 2
    expected_page_size = 20

    category = CategoryFactory()
    session.add(category)
    session.commit()

    session.bulk_save_objects(
        ItemFactory.create_batch(expected_items, category_id=category.id)
    )
    session.commit()

    response = client.get(
        f"{route}?page={expected_page}&page_size={expected_page_size}"
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_items_in_page_2
    assert response.json()["total"] == expected_items

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_page
    assert response.json()["page_size"] == expected_page_size


def test_create_item_should_return_201_and_generated_data_with_default_values(
    client, session
):
    route = "/v1/item/"

    category = CategoryFactory()
    session.add(category)
    session.commit()

    item_data = {
        "name": "Item 1",
        "description": "Item 1 description",
        "category_id": category.id,
    }

    response = client.post(route, json=item_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["result"]["name"] == item_data["name"]
    assert response.json()["result"]["description"] == item_data["description"]
    assert response.json()["result"]["is_active"] is True
    assert response.json()["result"]["category_id"] == category.id
    assert response.json()["result"]["minimum_threshold"] == 0
    assert response.json()["result"]["stock_quantity"] == 0
    assert "id" in response.json()["result"]
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_create_item_should_return_201_and_generated_data(client, session):
    route = "/v1/item/"

    category = CategoryFactory()
    session.add(category)
    session.commit()

    item_data = {
        "name": "Item 1",
        "description": "Item 1 description",
        "category_id": category.id,
        "minimum_threshold": 10,
        "stock_quantity": 20,
    }

    response = client.post(route, json=item_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["result"]["name"] == item_data["name"]
    assert response.json()["result"]["description"] == item_data["description"]
    assert response.json()["result"]["is_active"] is True
    assert response.json()["result"]["category_id"] == category.id
    assert (
        response.json()["result"]["minimum_threshold"]
        == item_data["minimum_threshold"]
    )
    assert (
        response.json()["result"]["stock_quantity"]
        == item_data["stock_quantity"]
    )
    assert "id" in response.json()["result"]
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_read_item_should_return_200_and_generated_data(session, client):
    route = "/v1/item/"

    category = CategoryFactory()
    session.add(category)
    session.commit()

    item = ItemFactory(category_id=category.id)
    session.add(item)
    session.commit()

    response = client.get(f"{route}{item.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == item.name
    assert response.json()["result"]["description"] == item.description
    assert response.json()["result"]["is_active"] == item.is_active
    assert response.json()["result"]["id"] == item.id
    assert response.json()["result"]["category_id"] == item.category_id
    assert (
        response.json()["result"]["minimum_threshold"]
        == item.minimum_threshold
    )
    assert response.json()["result"]["stock_quantity"] == item.stock_quantity
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_update_item_should_return_200_and_updated_data(session, client):
    route = "/v1/item/"
    category = CategoryFactory()
    session.add(category)
    session.commit()

    item = ItemFactory(category_id=category.id)
    session.add(item)
    session.commit()

    item_data = {
        "name": "Item 1 updated",
        "description": "Item 1 description updated",
        "is_active": False,
        "category_id": item.category_id,
        "minimum_threshold": 10,
        "stock_quantity": 20,
    }

    response = client.put(f"{route}{item.id}", json=item_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == item_data["name"]
    assert response.json()["result"]["description"] == item_data["description"]
    assert response.json()["result"]["is_active"] == item_data["is_active"]
    assert response.json()["result"]["category_id"] == item_data["category_id"]
    assert (
        response.json()["result"]["minimum_threshold"]
        == item_data["minimum_threshold"]
    )
    assert (
        (response.json()["result"]["stock_quantity"])
        == item_data["stock_quantity"]
    )
    assert response.json()["result"]["id"] == item.id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]
    assert (
        response.json()["result"]["updated_at"]
        != response.json()["result"]["created_at"]
    )


def test_delete_item_should_return_200_and_deleted_message(session, client):
    route = "/v1/item/"

    category = CategoryFactory()
    session.add(category)
    session.commit()

    item = ItemFactory(category_id=category.id)
    session.add(item)
    session.commit()

    response = client.delete(f"{route}{item.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Resource deleted successfully."
    assert response.json()["id"] == item.id
    assert response.json()["resource"] == AppResource.ITEM.value


def test_item_not_found_exception_should_return_404(client):
    route = "/v1/item/"
    random_id = "56f0572c-1dec-4b4d-b517-4cac967146a7"
    response = client.get(f"{route}{random_id}")

    exception = ResourceNotFound(resource=AppResource.ITEM)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == f"{route}{random_id}"


def test_invalid_id_exception_should_return_422(client):
    route = "/v1/item/"
    invalid_input = "invalid-id"
    response = client.get(f"{route}{invalid_input}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["input"] == invalid_input
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, value should be a valid UUID"
    )


def test_item_name_already_exists_exception_should_return_422(session, client):
    route = "/v1/item/"
    category = CategoryFactory()
    session.add(category)
    session.commit()

    item = ItemFactory(category_id=category.id)
    session.add(item)
    session.commit()

    item_data = {
        "name": item.name,
        "category_id": item.category_id,
        "minimum_threshold": 10,
        "stock_quantity": 20,
    }

    response = client.post(route, json=item_data)

    exception = ItemNameAlreadyExists()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == route
