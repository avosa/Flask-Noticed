import firebase_admin
from firebase_admin import credentials, messaging
from celery import shared_task


class FCM:
    @staticmethod
    def deliver(notification, config):
        cred_path = config["credentials_path"]
        device_token = config["device_token"]
        message = config["message"]

        send_fcm_message.delay(notification.id, cred_path, device_token, message)


@shared_task
def send_fcm_message(notification_id, cred_path, device_token, message):
    from ..models import Notification

    notification = Notification.query.get(notification_id)

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    message = messaging.Message(
        data=message,
        token=device_token,
    )
    response = messaging.send(message)
    print(f"Successfully sent message: {response}")
