from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..settings import AppSettings

settings = AppSettings()
engine = create_engine(settings.DB_URL, echo=True)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
