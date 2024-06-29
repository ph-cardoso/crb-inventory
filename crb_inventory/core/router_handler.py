from fastapi import FastAPI

from ..routers.v1 import category, tag


def include_routers_v1(app: FastAPI):
    # v1 routes
    app.include_router(category.router)
    app.include_router(tag.router)
    return app
