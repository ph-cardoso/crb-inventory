from http import HTTPStatus

from fastapi import HTTPException


class CustomFieldNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Custom field name already exists."
        self.error_code = "005"
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )
