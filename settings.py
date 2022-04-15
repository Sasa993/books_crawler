import hjson

with open('main.conf', mode='r', encoding='utf-8') as config_file:
	contents_config_file = config_file.read()
config = hjson.loads(contents_config_file)

pushbullet_api = config['apis']['pushbullet']
url = config['megasrbija']['url']
username = config['megasrbija']['username']
password = config['megasrbija']['password']
