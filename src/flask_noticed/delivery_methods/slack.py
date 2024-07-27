import os
import requests
import redis
from celery import shared_task


class Slack:
    DEFAULT_URL = "https://slack.com/api/chat.postMessage"

    @staticmethod
    def deliver(notification, config):
        json_data = config.get("json")
        url = config.get("url", Slack.DEFAULT_URL)
        headers = config.get(
            "headers", {"Authorization": f"Bearer {os.getenv('SLACK_API_TOKEN')}"}
        )

        send_slack_message.delay(notification.id, url, json_data, headers)


@shared_task
def send_slack_message(notification_id, url, json_data, headers):
    from ..models import Notification

    notification = Notification.query.get(notification_id)

    response = requests.post(url, json=json_data, headers=headers)
    response.raise_for_status()
