import pytest
from unittest.mock import patch
from flask_noticed.models import Event, Notification
from flask_noticed.delivery_methods.slack import Slack


@pytest.fixture
def mock_slack_post():
    with patch("flask_noticed.delivery_methods.slack.requests.post") as mock_post:
        mock_post.return_value.raise_for_status.return_value = None
        yield mock_post


def test_slack_deliver(db_session, mock_slack_post, mock_celery):
    event = Event(type="test_event")
    db_session.add(event)
    db_session.commit()

    notification = Notification(event=event, recipient_type="User", recipient_id=1)
    db_session.add(notification)
    db_session.commit()

    config = {
        "json": {"text": "Test message"},
        "url": "https://slack.com/api/chat.postMessage",
    }

    Slack.deliver(notification, config)
    mock_celery.assert_called_once()
