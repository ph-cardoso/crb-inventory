# Create a exception handler function to handle exceptions in fastapi.

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..models.exceptions.resource_utils import InvalidId, ResourceNotFound


def include_exceptions(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):  # pragma: no cover
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
    async def resource_not_found_exception_handler(request, exc):
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

    @app.exception_handler(InvalidId)
    async def invalid_id_exception_handler(request, exc):
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
