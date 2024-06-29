from http import HTTPStatus

from fastapi import HTTPException


class TagNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Tag name already exists."
        self.error_code = "004"
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )


# - lowercase
# - alphanumeric characters
# - separated by hyphens
# - Maximun length of 50 characters
class InvalidTagName(HTTPException):
    def __init__(self, value: str):
        detail = f"Invalid tag name. Received: {value}. Expected: Lowercase alphanumeric characters separated by hyphens with a max length of 50 characters."  # noqa: E501
        self.error_code = "005"
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )
