import hjson

with open('main.conf', mode='r', encoding='utf-8') as config_file:
    contents_config_file = config_file.read()
config = hjson.loads(contents_config_file)

api_endpoint = config['apis']['drf']
pushbullet_api = config['apis']['pushbullet_key']
url = config['megasrbija']['url']
username = config['megasrbija']['username']
password = config['megasrbija']['password']

book_types = {
    'audio': '89.0',
    'domestic': '188.0',
    'it': '154.0',
    'magazine': '73.0',
}

book_types_api = {
    'audio': 0,
    'domestic': 1,
    'it': 2,
    'magazine': 3,
}


db_ways = ['authors', 'books']
