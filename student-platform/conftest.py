import pytest
from studentapp import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///memory"


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(TestConfig)
    # flask_app = flask_app.test_client()  # user the Wierkzurg flask test client
    app_context = flask_app.app_context()
    app_context.push()
    db.create_all()
    yield flask_app

    # tear down activities
    app_context.pop()


@pytest.fixture(scope="module")
def test_db(test_client):
    with test_client.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


