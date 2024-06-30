import argparse
import logging
import logging.config
from settings import (
    book_types,
    book_types_api,
    url,
)
from utils.scraper import scrape, scrape_for_db
from utils.fill_db_apis import fill_db

logging.config.fileConfig(fname='loggers.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def scrape_bullet(args):
    full_url = url + book_types[args.type]
    scrape(full_url, args.type)


def scrape_fill_db(args):
    full_url = url + book_types[args.type]
    books_list = scrape_for_db(full_url, args.type, all_dates=args.all_dates)
    fill_db(books_list, book_types_api[args.type])


parser = argparse.ArgumentParser(
    description="""
    Crawl Megasrbija website and notify user with collected content.
    """
)
subparsers = parser.add_subparsers(required=True)

parser_scrape_bullet = subparsers.add_parser('scrape_bullet')
parser_scrape_bullet.add_argument(
    'type',
    choices=book_types.keys(),
    type=str,
    help="Select the type of book you would like to be notified about.",
)
parser_scrape_bullet.set_defaults(func=scrape_bullet)

parser_scrape_fill_db = subparsers.add_parser('scrape_fill_db')
parser_scrape_fill_db.add_argument(
    'type',
    choices=book_types.keys(),
    type=str,
    help="Select the type of book you would like to scrape for.",
)
parser_scrape_fill_db.add_argument(
    '--all_dates',
    action='store_true',
    help="If set, scrape for all dates."
)
parser_scrape_fill_db.set_defaults(func=scrape_fill_db)

args = parser.parse_args()
args.func(args)
