from http import HTTPStatus

from crb_inventory.models.exceptions.custom_field import (
    CustomFieldNameAlreadyExists,
)
from crb_inventory.models.exceptions.resource import (
    ResourceNotFound,
)
from crb_inventory.models.utils import AppResource
from tests.factories import CustomFieldFactory


def test_read_custom_fields_should_return_6(session, client):
    route = "/v1/custom_field/"
    expected_custom_fields = 6
    expected_default_page = 1
    expected_default_page_size = 10

    session.bulk_save_objects(
        CustomFieldFactory.create_batch(expected_custom_fields)
    )
    session.commit()

    response = client.get(route)

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_custom_fields
    assert response.json()["total"] == expected_custom_fields

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_default_page
    assert response.json()["page_size"] == expected_default_page_size


def test_read_custom_fields_should_return_5_in_page_2(session, client):
    route = "/v1/custom_field/"
    expected_custom_fields = 25
    expected_custom_fields_in_page_2 = 5
    expected_page = 2
    expected_page_size = 20

    session.bulk_save_objects(
        CustomFieldFactory.create_batch(expected_custom_fields)
    )
    session.commit()

    response = client.get(
        f"{route}?page={expected_page}&page_size={expected_page_size}"
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_custom_fields_in_page_2
    assert response.json()["total"] == expected_custom_fields

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_page
    assert response.json()["page_size"] == expected_page_size


def test_create_custom_field_should_return_201_and_generated_data(client):
    route = "/v1/custom_field/"
    custom_field_data = {
        "name": "custom_field_1",
        "description": "CustomField 1 description",
    }

    response = client.post(route, json=custom_field_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["result"]["name"] == custom_field_data["name"]
    assert (
        response.json()["result"]["description"]
        == custom_field_data["description"]
    )
    assert response.json()["result"]["is_active"] is True
    assert "id" in response.json()["result"]
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_read_custom_field_should_return_200_and_generated_data(
    session, client
):
    route = "/v1/custom_field/"
    custom_field = CustomFieldFactory()
    session.add(custom_field)
    session.commit()

    response = client.get(f"{route}{custom_field.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == custom_field.name
    assert response.json()["result"]["description"] == custom_field.description
    assert response.json()["result"]["is_active"] == custom_field.is_active
    assert response.json()["result"]["id"] == custom_field.id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_update_custom_field_should_return_200_and_updated_data(
    session, client
):
    route = "/v1/custom_field/"
    custom_field = CustomFieldFactory()
    session.add(custom_field)
    session.commit()

    custom_field_data = {
        "name": "custom_field_1_updated",
        "description": "CustomField 1 description updated",
        "is_active": False,
    }

    response = client.put(f"{route}{custom_field.id}", json=custom_field_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == custom_field_data["name"]
    assert (
        response.json()["result"]["description"]
        == custom_field_data["description"]
    )
    assert (
        response.json()["result"]["is_active"]
        == custom_field_data["is_active"]
    )
    assert response.json()["result"]["id"] == custom_field.id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]
    assert (
        response.json()["result"]["updated_at"]
        != response.json()["result"]["created_at"]
    )


def test_delete_custom_field_should_return_200_and_deleted_message(
    session, client
):
    route = "/v1/custom_field/"
    custom_field = CustomFieldFactory()
    session.add(custom_field)
    session.commit()

    response = client.delete(f"{route}{custom_field.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Resource deleted successfully."
    assert response.json()["id"] == custom_field.id
    assert response.json()["resource"] == AppResource.CUSTOM_FIELD.value


def test_custom_field_not_found_exception_should_return_404(client):
    route = "/v1/custom_field/"
    random_id = "56f0572c-1dec-4b4d-b517-4cac967146a7"
    response = client.get(f"{route}{random_id}")

    exception = ResourceNotFound(resource=AppResource.CUSTOM_FIELD)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == f"{route}{random_id}"


def test_invalid_id_exception_should_return_422(client):
    route = "/v1/custom_field/"
    invalid_input = "invalid-id"
    response = client.get(f"{route}{invalid_input}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(response.json()["detail"]) == 1
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["input"] == invalid_input


def test_custom_field_name_already_exists_exception_should_return_422(
    session, client
):
    route = "/v1/custom_field/"
    custom_field = CustomFieldFactory()
    session.add(custom_field)
    session.commit()

    custom_field_data = {
        "name": custom_field.name,
    }

    exception = CustomFieldNameAlreadyExists()

    response = client.post(route, json=custom_field_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == route


def test_custom_field_invalid_name_exception_should_return_422(client):
    route = "/v1/custom_field/"

    custom_field_data = {
        "name": "Invalid_Name",
    }

    response = client.post(route, json=custom_field_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(response.json()["detail"]) == 1
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["input"] == custom_field_data["name"]
