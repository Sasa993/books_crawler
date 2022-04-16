import logging
import mechanicalsoup
from bs4 import BeautifulSoup
from settings import (
    password,
    username,
)

logger = logging.getLogger(__name__)


def login_to_page(link: str) -> BeautifulSoup:
    """
    Login to page using mechanicalsoup.
    """
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
    )
    browser.open(link)
    try:
        browser.select_form("#main_content_section form")
    except mechanicalsoup.utils.LinkNotFoundError:
        logger.error("The login form has not been found.")
        return None
    # TODO: figure out if there is a way to check if the login was successful
    # or not and based on that write logs.
    browser['user'] = username
    browser['passwrd'] = password
    browser.submit_selected()
    return browser.page
