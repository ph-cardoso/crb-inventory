from http import HTTPStatus

from fastapi import HTTPException


class CustomFieldNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Custom field name already exists."
        self.error_code = "005"
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )


class InvalidCustomFieldName(HTTPException):
    def __init__(self, value: str):
        detail = f"Invalid custom field name. Received: {value}. Expected: Lowercase alphanumeric characters separated by underscores with a max length of 30 characters."  # noqa: E501
        self.error_code = "006"
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )
