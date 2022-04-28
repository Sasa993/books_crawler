"""
https://docs.pushbullet.com/
"""
from pushbullet import Pushbullet
from settings import pushbullet_api


def send_notification(title: str, body: str) -> None:
    """
    Send notification via Pushbullet.
    """
    pb = Pushbullet(pushbullet_api)
    pb.push_note(title, body)
