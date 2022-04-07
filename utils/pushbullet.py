"""
todo: PUSHBULLET with API requests: https://docs.pushbullet.com/
"""
# import hjson
from pushbullet import Pushbullet
from settings import pushbullet_api

# Sending notification via pushbullet
def send_notification(title: str, body: str) -> None:
	pb = Pushbullet(pushbullet_api)
	push = pb.push_note(title, body)