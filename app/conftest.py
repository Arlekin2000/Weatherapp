import pytest


@pytest.fixture(scope='session')
def app():
    from app.main import app
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def db():
    from app.models import db, User, UserHistory, City

    db.create_tables([User, UserHistory, City])
    yield db
    db.drop_tables([User, UserHistory, City])


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()
