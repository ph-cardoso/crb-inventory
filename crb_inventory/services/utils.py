from uuid import UUID


def validate_uuid(uuid: str) -> bool:
    try:
        UUID(uuid)
    except ValueError:
        return False
    return True
