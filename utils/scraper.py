import argparse
import logging
import re
from datetime import date, timedelta
from utils.calendar import convert_to_target_format
from utils.login import login_to_page
from utils.pushbullet import send_notification

logger = logging.getLogger(__name__)

yesterday = convert_to_target_format(date.today() - timedelta(7))  # todo
main_div = {'name': 'div', 'attrs': {'id': 'messageindex'}}
undesired_td = {
    'name': 'td',
    'attrs': {
        'class': ['stickybg', 'stickybg2']
    }
}
desired_td = {'name': 'td', 'attrs': {'class': 'lastpost'}}
subject_td = {'name': 'td', 'attrs': {'class': 'subject'}}


def scrape(
    link: str,
    subject_name: argparse.Namespace,
) -> None:
    """
    Crawl Megasrbija website and collect desired content.
    Collect only books/magazines that have been published
    day before - yesterday and use Pushbullet to notify user.
    """
    logger.debug(f"Starting to scrape for {subject_name}; url: {link}")
    book_counter = 0
    books_list = {}
    soup = login_to_page(link)
    if soup is None:
        return
    try:
        start = soup.find(**main_div).table.tbody
    except AttributeError:
        log_msg = 'Could not find(scrape) the "table.body" of the'\
            f' following search parametars: \n"{main_div.values()}".'
        logger.error(log_msg)
        return None

    for book in start.find_all("tr")[1:]:
        if book.find(**undesired_td):
            continue
        lastpost = book.find(**desired_td).text.split()
        # avoid looping through today's published books/magazines
        if ("danas" not in lastpost):
            published_date = (
                f'{lastpost[0]} {lastpost[1]} '
                f'{lastpost[2].rstrip(",")}'
            )
            if (published_date == yesterday):
                title = book.find(**subject_td).div.span.a.text
                # the delimiter could be '-' or '–' for now
                title_tmp = re.split(r"[-–]", title, maxsplit=1)
                book_link = book.find(**subject_td).div.span.a['href']
                books_list[book_counter] = {}
                books_list[book_counter]['author'] = title_tmp[0]
                books_list[book_counter]['title'] = title_tmp[1]
                books_list[book_counter]['link'] = book_link
                book_counter += 1

    body = ""
    if (book_counter > 0):
        title = f"{book_counter} new {subject_name.title()} book/s added"\
            f" yesterday ({yesterday})!\n"
        for x in range(book_counter):
            body += f"Author: {books_list[x]['author']}\n"\
                f"Title: {books_list[x]['title']}\n"\
                f"Link: ({books_list[x]['link']})\n\n"

        try:
            send_notification(title, body)
            logger.info(f"Notification ({subject_name.title()}) has been sent"
                        " successfully")
        except Exception:
            logger.error("Notification sending failed!")


def scrape_for_db(
    link: str,
    subject_name: argparse.Namespace,
) -> None:
    """
    todo: continue here, you need to refactor this function, or even better,
    this can be achieved with one function only.
    """
    logger.debug(f"Starting to scrape for {subject_name}; url: {link}")
    book_counter = 0
    books_list = {}
    soup = login_to_page(link)
    if soup is None:
        return
    try:
        start = soup.find(**main_div).table.tbody
    except AttributeError:
        log_msg = 'Could not find(scrape) the "table.body" of the'\
            f' following search parametars: \n"{main_div.values()}".'
        logger.error(log_msg)
        return None

    for book in start.find_all("tr")[1:]:
        if book.find(**undesired_td):
            continue
        lastpost = book.find(**desired_td).text.split()
        # avoid looping through today's published books/magazines
        if ("danas" not in lastpost):
            published_date = (
                f'{lastpost[0]} {lastpost[1]} '
                f'{lastpost[2].rstrip(",")}'
            )
            if (published_date == yesterday):
                title = book.find(**subject_td).div.span.a.text
                # the delimiter could be '-' or '–' for now
                title_tmp = re.split(r"[-–]", title, maxsplit=1)
                book_link = book.find(**subject_td).div.span.a['href']
                books_list[book_counter] = {}
                books_list[book_counter]['author'] = title_tmp[0]
                books_list[book_counter]['title'] = title_tmp[1]
                books_list[book_counter]['link'] = book_link
                books_list[book_counter]['published_date'] = published_date
                book_counter += 1

    # authors = [item['author'] for item in books_list.values()]
    return books_list
