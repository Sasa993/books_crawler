import argparse
from settings import url
from utils.scraper import scrape

book_types = {
	'audio': '89.0',
	'domestic': '188.0',
	'it': '154.0',
	'magazine': '73.0',
}

parser = argparse.ArgumentParser(description='Todo todo well todo!')
parser.add_argument(
	"--type",
	choices=book_types.keys(),
	type=str,
	required=True,
	help="This is more info."
)
args = parser.parse_args()
full_url = url + book_types[args.type]
# print(1111, full_url, type(full_url))

scrape(full_url, 8, args.type)
# scrape('https://megasrbija.com/index.php?board=188.0', 8, 'Domestic Book')
# scrape('https://megasrbija.com/index.php?board=154.0', 7, 'IT Book') # todo: error
# scrape('https://megasrbija.com/index.php?board=73.0', 6, 'Magazine')