from http import HTTPStatus

from fastapi import FastAPI

from .core.exception_handler import include_exceptions
from .core.router_handler import include_routers_v1
from .settings import AppSettings

APP_DATA = {
    "name": "CRB Inventory API",
    "description": "API para gestão de inventário",
    "version_v1": "1.0.0",
    "latest_version": "0.1.0",
    "docs": "/docs",
    "docs_v1": "/v1/docs",
}


settings = AppSettings()

tags_metadata = [
    {
        "name": "v1",
        "description": "CRB Inventory API v1, doc link on the right",
        "externalDocs": {
            "description": "API v1 Documentation",
            "url": f"{settings.APP_URL}{APP_DATA["docs_v1"]}",
        },
    }
]

app = FastAPI(
    title=APP_DATA["name"],
    description=APP_DATA["description"],
    openapi_tags=tags_metadata,
)


@app.get(
    "/",
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
async def root_endpoint():
    return {
        "api_name": APP_DATA["name"],
        "version": APP_DATA["latest_version"],
        "docs": APP_DATA["docs"],
    }


v1 = FastAPI(
    title=APP_DATA["name"],
    description=APP_DATA["description"],
)
v1 = include_routers_v1(v1)
v1 = include_exceptions(v1)


@v1.get(
    "/",
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
async def v1_root_endpoint():
    return {
        "api_name": APP_DATA["name"],
        "version": APP_DATA["version_v1"],
        "docs": APP_DATA["docs_v1"],
    }


app.mount("/v1", v1, name="v1")
