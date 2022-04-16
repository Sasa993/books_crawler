from datetime import date, timedelta
import logging
from utils.calendar import convert_to_target_format
from utils.login import login_to_page
from utils.pushbullet import send_notification

logger = logging.getLogger(__name__)

yesterday = date.today() - timedelta(2)
yesterday = convert_to_target_format(yesterday)


def scrape(link, post_starts_at, subject_name) -> None:
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
        start = soup.find("div", {"id": "messageindex"}).table.tbody
    except AttributeError:
        log_msg = "TODO: could not find messageindex or the given table"\
            " or something similar."
        logger.error(log_msg)
        return None

    for book in start.find_all("tr")[post_starts_at:]:
        lastpost = book.find("td", class_="lastpost").text.split()
        # print(333, lastpost)
        # avoid looping through today's published books/magazines
        if ("danas" not in lastpost):
            published_date = (
                f'{lastpost[0]} {lastpost[1]} '
                f'{lastpost[2].rstrip(",")}'
            )

            if (published_date == yesterday):
                title = book.find("td", class_="subject").div.span.a.text
                published_time = lastpost[3]
                book_link = book.find("td", class_="subject").div.span.a['href']
                books_list[book_counter] = {}
                books_list[book_counter]['title'] = title
                books_list[book_counter]['date'] = published_date
                books_list[book_counter]['time'] = published_time
                books_list[book_counter]['link'] = book_link
                book_counter += 1

    body = ""
    if (book_counter > 0):
        title = f"{book_counter} new {subject_name.title()} book/s added\
            yesterday ({yesterday})!\n"
        for x in range(book_counter):
            body += f"{books_list[x]['title']}\
                ({books_list[x]['link']})\n\n"

        send_notification(title, body)
