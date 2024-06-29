from http import HTTPStatus

from crb_inventory.models.exceptions.resource import (
    InvalidId,
    ResourceNotFound,
)
from crb_inventory.models.exceptions.tag import (
    InvalidTagName,
    TagNameAlreadyExists,
)
from crb_inventory.models.utils import AppResource
from tests.factories import TagFactory


def test_read_tags_should_return_6(session, client):
    route = "/v1/tag/"
    expected_tags = 6
    expected_default_page = 1
    expected_default_page_size = 10

    session.bulk_save_objects(TagFactory.create_batch(expected_tags))
    session.commit()

    response = client.get(route)

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_tags
    assert response.json()["total"] == expected_tags

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_default_page
    assert response.json()["page_size"] == expected_default_page_size


def test_read_tags_should_return_5_in_page_2(session, client):
    route = "/v1/tag/"
    expected_tags = 25
    expected_tags_in_page_2 = 5
    expected_page = 2
    expected_page_size = 20

    session.bulk_save_objects(TagFactory.create_batch(expected_tags))
    session.commit()

    response = client.get(
        f"{route}?page={expected_page}&page_size={expected_page_size}"
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["result"]) == expected_tags_in_page_2
    assert response.json()["total"] == expected_tags

    # Validating default values of page and page_size
    assert response.json()["page"] == expected_page
    assert response.json()["page_size"] == expected_page_size


def test_create_tag_should_return_201_and_generated_data(client):
    route = "/v1/tag/"
    tag_data = {
        "name": "tag-1",
        "description": "Tag 1 description",
    }

    response = client.post(route, json=tag_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["result"]["name"] == tag_data["name"]
    assert response.json()["result"]["description"] == tag_data["description"]
    assert response.json()["result"]["is_active"] is True
    assert "public_id" in response.json()["result"]
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_read_tag_should_return_200_and_generated_data(session, client):
    route = "/v1/tag/"
    tag = TagFactory()
    session.add(tag)
    session.commit()

    response = client.get(f"{route}{tag.public_id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == tag.name
    assert response.json()["result"]["description"] == tag.description
    assert response.json()["result"]["is_active"] == tag.is_active
    assert response.json()["result"]["public_id"] == tag.public_id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_update_tag_should_return_200_and_updated_data(session, client):
    route = "/v1/tag/"
    tag = TagFactory()
    session.add(tag)
    session.commit()

    tag_data = {
        "name": "tag-1-updated",
        "description": "Tag 1 description updated",
        "is_active": False,
    }

    response = client.put(f"{route}{tag.public_id}", json=tag_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == tag_data["name"]
    assert response.json()["result"]["description"] == tag_data["description"]
    assert response.json()["result"]["is_active"] == tag_data["is_active"]
    assert response.json()["result"]["public_id"] == tag.public_id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]
    assert (
        response.json()["result"]["updated_at"]
        != response.json()["result"]["created_at"]
    )


def test_delete_tag_should_return_200_and_deleted_message(session, client):
    route = "/v1/tag/"
    tag = TagFactory()
    session.add(tag)
    session.commit()

    response = client.delete(f"{route}{tag.public_id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Resource deleted successfully."
    assert response.json()["public_id"] == tag.public_id
    assert response.json()["resource"] == AppResource.TAG.value


def test_tag_not_found_exception_should_return_404(client):
    route = "/v1/tag/"
    random_id = "56f0572c-1dec-4b4d-b517-4cac967146a7"
    response = client.get(f"{route}{random_id}")

    exception = ResourceNotFound(resource=AppResource.TAG)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == f"{route}{random_id}"


def test_invalid_id_exception_should_return_400(client):
    route = "/v1/tag/"
    invalid_id = "invalid-id"
    response = client.get(f"{route}{invalid_id}")

    exception = InvalidId(value=invalid_id)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == f"{route}{invalid_id}"


def test_tag_name_already_exists_exception_should_return_422(session, client):
    route = "/v1/tag/"
    tag = TagFactory()
    session.add(tag)
    session.commit()

    tag_data = {
        "name": tag.name,
    }

    exception = TagNameAlreadyExists()

    response = client.post(route, json=tag_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == route


def test_tag_invalid_name_exception_should_return_422(client):
    route = "/v1/tag/"

    tag_data = {
        "name": "Invalid_Name",
    }

    exception = InvalidTagName(value=tag_data["name"])

    response = client.post(route, json=tag_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["exc"] == exception.__class__.__name__
    assert response.json()["detail"] == exception.detail
    assert response.headers["X-Error-Code"] == exception.error_code
    assert response.json()["url"] == route
