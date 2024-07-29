from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..models.exceptions.category import CategoryNameAlreadyExists
from ..models.exceptions.item import ItemNameAlreadyExists
from ..models.exceptions.resource import ResourceNotFound
from ..models.exceptions.tag import TagNameAlreadyExists


def include_exceptions(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_handler(request, exc):  # pragma: no cover
        return JSONResponse(
            status_code=500,
            content={
                "exc": exc.__class__.__name__,
                "error_code": "099",
                "detail": str(exc),
                "url": request.url.path,
            },
            headers={"X-Error-Code": "099"},
        )

    @app.exception_handler(ResourceNotFound)
    async def resource_not_found_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "exc": exc.__class__.__name__,
                "error_code": exc.error_code,
                "detail": exc.detail,
                "url": request.url.path,
            },
            headers={"X-Error-Code": exc.error_code},
        )

    @app.exception_handler(CategoryNameAlreadyExists)
    async def category_name_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "exc": exc.__class__.__name__,
                "error_code": exc.error_code,
                "detail": exc.detail,
                "url": request.url.path,
            },
            headers={"X-Error-Code": exc.error_code},
        )

    @app.exception_handler(TagNameAlreadyExists)
    async def tag_name_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "exc": exc.__class__.__name__,
                "error_code": exc.error_code,
                "detail": exc.detail,
                "url": request.url.path,
            },
            headers={"X-Error-Code": exc.error_code},
        )

    @app.exception_handler(ItemNameAlreadyExists)
    async def item_name_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "exc": exc.__class__.__name__,
                "error_code": exc.error_code,
                "detail": exc.detail,
                "url": request.url.path,
            },
            headers={"X-Error-Code": exc.error_code},
        )

    return app
