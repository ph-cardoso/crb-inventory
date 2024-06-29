from fastapi import FastAPI

from ..routers.v1 import category, custom_field, tag


def include_routers_v1(app: FastAPI):
    app.include_router(category.router)
    app.include_router(tag.router)
    app.include_router(custom_field.router)
    return app
