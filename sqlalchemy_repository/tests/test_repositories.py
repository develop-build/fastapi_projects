
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app import models
from app.repositories import UserRepository


@pytest.fixture
def repository():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        yield UserRepository(db)

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_create_user(repository):
    user = repository.create(
        name="Deepak",
        email="deepak@example.com",
    )

    assert user.id is not None
    assert user.name == "Deepak"
    assert user.email == "deepak@example.com"


def test_get_user_by_id(repository):
    created = repository.create("Deepak", "deepak@example.com")

    user = repository.get_by_id(created.id)

    assert user is not None
    assert user.name == "Deepak"


def test_get_user_by_email(repository):
    repository.create("Deepak", "deepak@example.com")

    user = repository.get_by_email("deepak@example.com")

    assert user is not None
    assert user.email == "deepak@example.com"


def test_get_missing_user(repository):
    assert repository.get_by_id(999) is None


def test_list_users(repository):
    repository.create("Deepak", "deepak@example.com")
    repository.create("Priya", "priya@example.com")

    users = repository.list_all()

    assert len(users) == 2
    assert [user.name for user in users] == ["Deepak", "Priya"]


def test_update_user(repository):
    created = repository.create("Deepak", "deepak@example.com")

    updated = repository.update(created.id, name="Deepak Kumar")

    assert updated is not None
    assert updated.name == "Deepak Kumar"
    assert updated.email == "deepak@example.com"


def test_delete_user(repository):
    created = repository.create("Deepak", "deepak@example.com")

    deleted = repository.delete(created.id)

    assert deleted is True
    assert repository.get_by_id(created.id) is None


def test_delete_missing_user(repository):
    assert repository.delete(999) is False
