from crb_inventory.main import APP_DATA


def test_api_root_info(client):
    response = client.get("/")

    assert response.json() == {
        "api_name": APP_DATA["name"],
        "version": APP_DATA["latest_version"],
        "docs": APP_DATA["docs"],
    }


def test_api_v1_root_info(client):
    response = client.get("/v1/")

    assert response.json() == {
        "api_name": APP_DATA["name"],
        "version": APP_DATA["version_v1"],
        "docs": APP_DATA["docs_v1"],
    }
