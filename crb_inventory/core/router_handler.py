from fastapi import FastAPI

from ..routers.v1 import category, custom_field, item, tag


def include_routers_v1(app: FastAPI):
    app.include_router(category.router)
    app.include_router(tag.router)
    app.include_router(custom_field.router)
    app.include_router(item.router)
    return app
