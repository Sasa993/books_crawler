import requests
import logging

from datetime import datetime
from typing import Any, Dict

from settings import api_endpoint, api_auth_token


HEADERS = {
    'Authorization': f'Token {api_auth_token}'
}

logging.basicConfig(level=logging.INFO)


def get_existing_item_id(item: str, item_data: Dict[str, Any]) -> int:
    """
    todo
    """
    response = requests.get(
        f"{api_endpoint}/{item}s/",
        headers=HEADERS,
        params={'name': item_data.get('name')}
    )
    return response.json()[0]['id']


def handle_api_response(
    item: str,
    item_data: Dict[str, Any],
    response: requests.Response,
    success_msg: str
) -> None:
    """
    Handle API response dynamically.
    """
    if response.status_code == 201:
        # Item was created successfully
        logging.info(success_msg)
    elif response.status_code == 400:
        # Check if the response contains validation errors
        error_response = response.json()
        if 'name' in error_response and f'{item} with this name already exists.' in error_response['name']:
            # Item already exists, fetch the existing item ID instead
            existing_item_id = get_existing_item_id(item, item_data)
            return existing_item_id
    else:
        logging.error("API request failed with "
                      f"status code {response.status_code}")
        logging.error(response.text)
        # Raise an exception for non-2xx status codes
        response.raise_for_status()


def fill_authors(author_name: str) -> int:
    """
    Fill db with authors.
    """ 
    author_data = {"name": author_name}
    response = requests.post(
        f"{api_endpoint}/authors/",
        headers=HEADERS,
        data=author_data
    )
    handle_api_response('author', author_data, response, "Author created successfully.")
    return response.json().get('id')


def fill_books(
    author_id: int,
    book_type_id: int,
    link: str,
    book_name: str,
    published_date
) -> None:
    """
    Fill db with books.
    """
    pd = datetime.strptime(published_date, '%d %b %Y')
    book_data = {
        "author": author_id,
        "book_type": book_type_id,
        "link": link,
        "name": book_name,
        "published_date": pd.strftime('%Y-%m-%d'),
    }
    response = requests.post(
        f"{api_endpoint}/books/",
        headers=HEADERS,
        data=book_data
    )
    handle_api_response('book', book_data, response, "Book created successfully.")


def fill_db(books_list: dict, book_type: int) -> None:
    """
    todo
    """
    for book in books_list.values():
        author_id = fill_authors(book['author'])
        fill_books(author_id, book_type, book['link'], book['title'], book['published_date'])
