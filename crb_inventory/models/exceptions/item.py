from http import HTTPStatus

from fastapi import HTTPException


class ItemNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Item name already exists."
        self.error_code = "007"
        super().__init__(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail)
