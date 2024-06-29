from http import HTTPStatus

from fastapi import HTTPException


class CategoryNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Category name already exists."
        self.error_code = "003"
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )
