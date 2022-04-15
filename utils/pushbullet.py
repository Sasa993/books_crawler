"""
todo: PUSHBULLET with API requests: https://docs.pushbullet.com/
"""
# import hjson
from pushbullet import Pushbullet
from settings import pushbullet_api


def send_notification(title: str, body: str) -> None:
    """
    Send notificaiton via Pushbullet.
    """
    pb = Pushbullet(pushbullet_api)
    pb.push_note(title, body)
