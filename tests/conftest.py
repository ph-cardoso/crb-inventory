import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from crb_inventory.core.database import get_session
from crb_inventory.database_schema import mapper_registry
from crb_inventory.main import app, v1


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:15", driver="psycopg2") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        v1.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
    v1.dependency_overrides.clear()


@pytest.fixture()
def session(engine):
    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    mapper_registry.metadata.drop_all(engine)
