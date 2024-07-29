from http import HTTPStatus

import pytest

from crb_inventory.models.exceptions.resource import (
    ResourceNotFound,
)
from crb_inventory.models.exceptions.tag import (
    TagNameAlreadyExists,
)
from crb_inventory.models.utils import AppResource
from crb_inventory.services.tag import check_tag_exists, check_tag_name_exists
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
    assert "id" in response.json()["result"]
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_read_tag_should_return_200_and_generated_data(session, client):
    route = "/v1/tag/"
    tag = TagFactory()
    session.add(tag)
    session.commit()

    response = client.get(f"{route}{tag.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == tag.name
    assert response.json()["result"]["description"] == tag.description
    assert response.json()["result"]["is_active"] == tag.is_active
    assert response.json()["result"]["id"] == tag.id
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

    response = client.put(f"{route}{tag.id}", json=tag_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == tag_data["name"]
    assert response.json()["result"]["description"] == tag_data["description"]
    assert response.json()["result"]["is_active"] == tag_data["is_active"]
    assert response.json()["result"]["id"] == tag.id
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

    response = client.delete(f"{route}{tag.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Resource deleted successfully."
    assert response.json()["id"] == tag.id
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


def test_invalid_id_exception_should_return_422(client):
    route = "/v1/tag/"
    invalid_input = "invalid-id"
    response = client.get(f"{route}{invalid_input}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(response.json()["detail"]) == 1
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["input"] == invalid_input


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

    response = client.post(route, json=tag_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(response.json()["detail"]) == 1
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["input"] == tag_data["name"]


def test_patch_tag_should_return_200_and_updated_tag(session, client):
    route = "/v1/tag/"
    tag = TagFactory()
    session.add(tag)
    session.commit()

    tag_patch_data = {
        "name": "tag-updated",
        "description": "Tag 1 description updated",
        "is_active": False,
    }

    response = client.patch(f"{route}{tag.id}", json=tag_patch_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"]["name"] == tag_patch_data["name"]
    assert response.json()["result"]["description"] == tag_patch_data["description"]
    assert response.json()["result"]["is_active"] == tag_patch_data["is_active"]
    assert response.json()["result"]["id"] == tag.id
    assert "created_at" in response.json()["result"]
    assert "updated_at" in response.json()["result"]


def test_check_tag_name_exists(session):
    tag = TagFactory()
    session.add(tag)
    session.commit()

    tag_data = {"name": tag.name}

    check_tag_name_exists(tag_data["name"], session, tag.id)

    with pytest.raises(TagNameAlreadyExists):
        check_tag_name_exists(tag_data["name"], session)


def test_check_tag_exists(session):
    random_id = "56f0572c-1dec-4b4d-b517-4cac967146a7"

    tag = TagFactory()
    session.add(tag)
    session.commit()

    tag_checked = check_tag_exists(tag.id, session)
    assert tag_checked.id == tag.id
    assert tag_checked.name == tag.name

    with pytest.raises(ResourceNotFound):
        check_tag_exists(random_id, session)
