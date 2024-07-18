import re

from ..services.uuid import validate_uuid


def validate_positive_value(value: int | None) -> int | None:
    if value is not None and value < 0:
        raise ValueError(
            "value should be greater than or equal to 0"
        )  # pragma: no cover

    return value


def validate_uuid_value(value: str) -> str:
    if not validate_uuid(value):
        raise ValueError("value should be a valid UUID")  # pragma: no cover

    return value


def validate_custom_field_name_value(value: str) -> str:
    max_custom_field_length = 30
    regex = r"^[a-z0-9]+(_[a-z0-9]+)*$"

    if len(value) > max_custom_field_length:
        raise ValueError(
            "value should have a max length of "
            + str(max_custom_field_length)
            + " characters"
        )  # pragma: no cover

    if not re.match(regex, value):
        raise ValueError(
            "value should be in the format of lowercase alphanumeric "
            "characters separated by underscores"
        )  # pragma: no cover

    return value


def validate_tag_name_value(value: str) -> str:
    max_tag_length = 50
    regex = r"^[a-z0-9]+(-[a-z0-9]+)*$"

    if len(value) > max_tag_length:
        raise ValueError(
            "value should have a max length of "
            + str(max_tag_length)
            + " characters"
        )  # pragma: no cover

    if not re.match(regex, value):
        raise ValueError(
            "value should be in the format of lowercase alphanumeric "
            "characters separated by underscores"
        )  # pragma: no cover

    return value
