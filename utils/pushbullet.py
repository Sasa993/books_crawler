"""
todo: PUSHBULLET with API requests: https://docs.pushbullet.com/
"""
from pushbullet import Pushbullet

# Sending notification via pushbullet
def send_notification(title: str, body: str) -> None:
	# pushbullet API
	pb = Pushbullet('o.LFXxy23PQ9fQZEeBCHukcHrt3Jez1MRd')
	push = pb.push_note(title, body)