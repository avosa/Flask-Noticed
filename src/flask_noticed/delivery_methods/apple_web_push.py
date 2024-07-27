import os
import jwt
import time
import requests
import redis
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from celery import shared_task


class AppleWebPush:
    @staticmethod
    def deliver(notification, config):
        bundle_id = config.get("bundle_id", os.getenv("APPLE_PUSH_BUNDLE_ID"))
        team_id = config.get("team_id", os.getenv("APPLE_PUSH_TEAM_ID"))
        key_id = config.get("key_id", os.getenv("APPLE_PUSH_KEY_ID"))
        private_key = config.get("private_key", os.getenv("APPLE_PUSH_PRIVATE_KEY"))
        push_type = config.get("push_type", "alert")
        topic = f"{bundle_id}.push-type.{push_type}"
        device_token = config["device_token"]
        payload = config["payload"]

        send_apple_web_push.delay(
            notification.id,
            bundle_id,
            team_id,
            key_id,
            private_key,
            topic,
            device_token,
            payload,
        )


@shared_task
def send_apple_web_push(
    notification_id,
    bundle_id,
    team_id,
    key_id,
    private_key,
    topic,
    device_token,
    payload,
):
    from ..models import Notification

    notification = Notification.query.get(notification_id)

    token = create_token(team_id, key_id, private_key)
    headers = {
        "authorization": f"bearer {token}",
        "apns-topic": topic,
    }
    url = f"https://api.push.apple.com/3/device/{device_token}"

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()


def create_token(team_id, key_id, private_key):
    private_key = serialization.load_pem_private_key(
        private_key.encode(),
        password=None,
    )

    token = jwt.encode(
        {"iss": team_id, "iat": time.time()},
        private_key,
        algorithm="ES256",
        headers={
            "kid": key_id,
        },
    )
    return token
