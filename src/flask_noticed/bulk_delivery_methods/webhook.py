import requests
from celery import shared_task


class Webhook:
    @staticmethod
    def deliver(event, config):
        url = config.get("url")
        basic_auth = config.get("basic_auth")
        headers = config.get("headers", {})
        json_data = config.get("json")
        form_data = config.get("form")

        send_webhook.delay(event.id, url, basic_auth, headers, json_data, form_data)


@shared_task
def send_webhook(event_id, url, basic_auth, headers, json_data, form_data):
    from ..models import Event

    event = Event.query.get(event_id)

    auth = None
    if basic_auth:
        auth = (basic_auth["user"], basic_auth["pass"])

    response = requests.post(
        url, auth=auth, headers=headers, json=json_data, data=form_data
    )
    response.raise_for_status()
