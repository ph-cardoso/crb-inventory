from http import HTTPStatus

from fastapi import HTTPException

from ..utils import AppResource


class ResourceNotFound(HTTPException):
    def __init__(self, resource: AppResource):
        detail = f"{resource.value.capitalize()} not found."
        self.error_code = "001"
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


class InvalidId(HTTPException):
    def __init__(self, value: str):
        detail = f"Invalid resource ID. UUID v4 expected, but got {value}."
        self.error_code = "002"
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)
