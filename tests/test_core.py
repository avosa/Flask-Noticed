import pytest
from flask_noticed import db
from flask_noticed.models import Event, Notification


def test_create_app(app):
    assert app.config["TESTING"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_db_initialization(app, db_session):
    with app.app_context():
        assert db.metadata.tables.keys() == {"noticed_events", "noticed_notifications"}


def test_event_notification_relationship(db_session):
    event = Event(type="test_event")
    db_session.add(event)
    db_session.commit()

    notification1 = Notification(event=event, recipient_type="User", recipient_id=1)
    notification2 = Notification(event=event, recipient_type="User", recipient_id=2)
    db_session.add(notification1)
    db_session.add(notification2)
    db_session.commit()

    assert len(event.notifications) == 2
    assert event.notifications[0].recipient_id == 1
    assert event.notifications[1].recipient_id == 2


def test_notification_cascade_delete(db_session):
    event = Event(type="test_event")
    db_session.add(event)
    db_session.commit()

    notification1 = Notification(event=event, recipient_type="User", recipient_id=1)
    notification2 = Notification(event=event, recipient_type="User", recipient_id=2)
    db_session.add(notification1)
    db_session.add(notification2)
    db_session.commit()

    assert db_session.query(Notification).count() == 2

    db_session.delete(event)
    db_session.commit()

    assert db_session.query(Notification).count() == 0
