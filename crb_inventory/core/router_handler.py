from fastapi import FastAPI

from ..routers.v1 import category


def include_routers_v1(app: FastAPI):
    # v1 routes
    app.include_router(category.router)
    return app
