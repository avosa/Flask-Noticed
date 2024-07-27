import pytest
from flask_noticed.models import Event, Notification


def test_event_creation(db_session):
    event = Event(type="test_event", params={"key": "value"})
    db_session.add(event)
    db_session.commit()

    assert event.id is not None
    assert event.type == "test_event"
    assert event.params == {"key": "value"}


def test_notification_creation(db_session):
    event = Event(type="test_event")
    db_session.add(event)
    db_session.commit()

    notification = Notification(event=event, recipient_type="User", recipient_id=1)
    db_session.add(notification)
    db_session.commit()

    assert notification.id is not None
    assert notification.event_id == event.id
    assert notification.recipient_type == "User"
    assert notification.recipient_id == 1


def test_notification_read_unread(db_session):
    event = Event(type="test_event")
    notification = Notification(event=event, recipient_type="User", recipient_id=1)
    db_session.add(notification)
    db_session.commit()

    assert notification.unread
    assert not notification.read

    notification.mark_as_read()
    db_session.refresh(notification)

    assert notification.read
    assert not notification.unread

    notification.mark_as_unread()
    db_session.refresh(notification)

    assert notification.unread
    assert not notification.read


def test_notification_seen_unseen(db_session):
    event = Event(type="test_event")
    notification = Notification(event=event, recipient_type="User", recipient_id=1)
    db_session.add(notification)
    db_session.commit()

    assert notification.unseen
    assert not notification.seen

    notification.mark_as_seen()
    db_session.refresh(notification)

    assert notification.seen
    assert not notification.unseen

    notification.mark_as_unseen()
    db_session.refresh(notification)

    assert notification.unseen
    assert not notification.seen
