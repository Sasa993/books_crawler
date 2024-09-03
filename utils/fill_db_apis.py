import requests
import logging

from typing import Optional

from settings import api_endpoint, api_auth_token
from utils.calendar import parse_serbian_date


HEADERS = {
    'Authorization': f'Token {api_auth_token}'
}

logging.basicConfig(level=logging.INFO)


def get_existing_author_id(author_name: str) -> int:
    """
    todo
    """
    try:
        response = requests.get(
            f"{api_endpoint}/authors/",
            headers=HEADERS,
            params={'name': author_name}
        )
        author_id = next(
            (item['id'] for item in response.json() if item['name'] == author_name),  # noqa: E501
            None
        )
        return author_id
    except Exception:
        return None


def get_existing_book_id(author_name: str) -> int:
    """
    todo
    """
    try:
        response = requests.get(
            f"{api_endpoint}/authors/",
            headers=HEADERS,
            params={'name': author_name}
        )
        author_id = next(
            (item['id'] for item in response.json() if item['name'] == author_name),  # noqa: E501
            None
        )
        return author_id
    except Exception:
        return None


def fill_authors(author_name: str) -> Optional[int]:
    """
    Fill db with authors.
    """
    response = requests.post(
        f"{api_endpoint}/authors/",
        headers=HEADERS,
        data={"name": author_name}
    )

    if response.status_code == 201:
        # Item was created successfully
        logging.info("Author created successfully.")
        return response.json().get('id')
    elif response.status_code == 400:
        # Check if the response contains validation errors
        error_response = response.json()
        if (
            'name' in error_response and
            'author with this name already exists.' in error_response['name']
        ):
            # Item already exists, fetch the existing item ID instead
            logging.warn(f'Author {author_name} already exists.')
            existing_item_id = get_existing_author_id(author_name)
            return existing_item_id
        return None
    else:
        logging.error("API request failed with "
                      f"status code {response.status_code}")
        logging.error(response.text)
        # Raise an exception for non-2xx status codes
        response.raise_for_status()


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
    try:
        parsed_date = parse_serbian_date(published_date)
        book_data = {
            "author": author_id,
            "book_type": book_type_id,
            "link": link,
            "name": book_name,
            "published_date": parsed_date.strftime('%Y-%m-%d'),
        }
        response = requests.post(
            f"{api_endpoint}/books/",
            headers=HEADERS,
            data=book_data
        )

        if response.status_code == 201:
            # Item was created successfully
            logging.info("Book created successfully.")
        elif response.status_code == 400:
            logging.warn("Found some books duplicates. Skipping over them.")
        else:
            logging.error("API request failed with "
                          f"status code {response.status_code}")
            logging.error(response.text)
            # Raise an exception for non-2xx status codes
            response.raise_for_status()
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")


def fill_db(books_list: dict, book_type: int) -> None:
    """
    todo
    """
    for book in books_list.values():
        author_id = fill_authors(book['author'])
        fill_books(
            author_id,
            book_type,
            book['link'],
            book['title'],
            book['published_date']
        )
