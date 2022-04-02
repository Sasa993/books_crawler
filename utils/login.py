import mechanicalsoup
from bs4 import BeautifulSoup

def login_to_page(link: str) -> BeautifulSoup:
    """
    Login to page using mechanicalsoup.
    """
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
    )
    browser.open(link)
    browser.select_form("#main_content_section form")
    browser['user'] = 'smirgla'
    browser['passwrd'] = 'boozee11'
    resp = browser.submit_selected()
    return browser.page