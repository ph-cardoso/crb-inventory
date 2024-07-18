from uuid import UUID

import uuid_utils as uuid


def generate_uuid_v7() -> str:
    return str(uuid.uuid7())


def validate_uuid(uuid: str) -> bool:
    try:
        UUID(uuid)
    except ValueError:
        return False
    return True
