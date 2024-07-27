from . import db
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime, timezone


class Event(db.Model):
    __tablename__ = "noticed_events"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    record_type = db.Column(db.String(255))
    record_id = db.Column(db.Integer)
    params = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    notifications_count = db.Column(db.Integer, default=0)

    notifications = db.relationship(
        "Notification", back_populates="event", cascade="all, delete-orphan"
    )


class Notification(db.Model):
    __tablename__ = "noticed_notifications"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("noticed_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    recipient_type = db.Column(db.String(255), nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    read_at = db.Column(db.DateTime)
    seen_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    event = db.relationship("Event", back_populates="notifications")

    @property
    def recipient(self):
        return self.recipient_type.query.get(self.recipient_id)

    def mark_as_read(self):
        self.read_at = datetime.now(timezone.utc)
        db.session.commit()

    def mark_as_unread(self):
        self.read_at = None
        db.session.commit()

    def mark_as_seen(self):
        self.seen_at = datetime.now(timezone.utc)
        db.session.commit()

    def mark_as_unseen(self):
        self.seen_at = None
        db.session.commit()

    @property
    def read(self):
        return self.read_at is not None

    @property
    def unread(self):
        return self.read_at is None

    @property
    def seen(self):
        return self.seen_at is not None

    @property
    def unseen(self):
        return self.seen_at is None
