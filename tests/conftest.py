from unittest.mock import patch
import pytest
from flask_noticed import create_app, db
from flask_noticed.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def app():
    app, _ = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture(autouse=True)
def mock_celery():
    with patch("celery.app.task.Task.delay") as mock:
        yield mock
