from http import HTTPStatus

from fastapi import HTTPException


class ItemNameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Item name already exists."
        self.error_code = "007"
        super().__init__(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail)


class TagNotAssociatedWithItem(HTTPException):
    def __init__(self, tag_id: str, item_id: str):
        detail = "Tag is not associated with the item."
        self.error_code = "040"
        self.tag_id = tag_id
        self.item_id = item_id
        super().__init__(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail)


class TagAlreadyAssociatedWithItem(HTTPException):
    def __init__(self, tag_id: str, item_id: str):
        detail = "Tag is already associated with the item."
        self.error_code = "041"
        self.tag_id = tag_id
        self.item_id = item_id
        super().__init__(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail)
