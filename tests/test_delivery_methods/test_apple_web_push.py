import pytest
from unittest.mock import patch, Mock
from flask_noticed.models import Event, Notification
from flask_noticed.delivery_methods.apple_web_push import AppleWebPush


@pytest.fixture
def mock_apple_web_push_post():
    with patch(
        "flask_noticed.delivery_methods.apple_web_push.requests.post"
    ) as mock_post:
        mock_post.return_value.raise_for_status.return_value = None
        yield mock_post


@pytest.fixture
def mock_create_token():
    with patch(
        "flask_noticed.delivery_methods.apple_web_push.create_token"
    ) as mock_token:
        mock_token.return_value = "mocked_token"
        yield mock_token


def test_apple_web_push_deliver(
    db_session, mock_apple_web_push_post, mock_create_token, mock_celery
):
    event = Event(type="test_event")
    db_session.add(event)
    db_session.commit()

    notification = Notification(event=event, recipient_type="User", recipient_id=1)
    db_session.add(notification)
    db_session.commit()

    config = {
        "bundle_id": "com.example.app",
        "team_id": "TEAM123456",
        "key_id": "KEY123456",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMOCKED_PRIVATE_KEY\n-----END PRIVATE KEY-----",
        "device_token": "mocked_device_token",
        "payload": {"aps": {"alert": "Test message"}},
    }

    AppleWebPush.deliver(notification, config)
    mock_celery.assert_called_once()
