from http import HTTPStatus

from fastapi import HTTPException


class TagNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Tag name already exists."
        self.error_code = "004"
        super().__init__(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail)
