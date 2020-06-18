import pytest
from studentapp import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture(scope="module")
def test_client():
    app = create_app(TestConfig)
    flask_app = app.test_client()  # user the Wierkzurg flask test client
    app_context = app.app_context()
    app_context.push()
    yield flask_app

    # tear down activities
    app_context.pop()


@pytest.fixture(scope="module")
def test_db():
    db.create_all()
    yield db

    db.session.remove()
    db.drop_all()


