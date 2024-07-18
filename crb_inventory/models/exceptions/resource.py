from http import HTTPStatus

from fastapi import HTTPException

from ..utils import AppResource


class ResourceNotFound(HTTPException):
    def __init__(self, resource: AppResource):
        detail = f"{resource.value.capitalize()} not found."
        self.error_code = "001"
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)
