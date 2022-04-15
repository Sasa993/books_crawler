import argparse
from settings import (
    book_types,
    url,
)
from utils.scraper import scrape

parser = argparse.ArgumentParser(
    description="""
        Crawl Megasrbija website and notify user with collected content.
    """
)
parser.add_argument(
    "--type",
    choices=book_types.keys(),
    type=str,
    required=True,
    help="Select the type of book you would like to be notified about."
)
args = parser.parse_args()
full_url = url + book_types[args.type]

scrape(full_url, 8, args.type)
# scrape('https://megasrbija.com/index.php?board=188.0', 8, 'Domestic Book')
# scrape('https://megasrbija.com/index.php?board=154.0', 7, 'IT Book')
# scrape('https://megasrbija.com/index.php?board=73.0', 6, 'Magazine')
