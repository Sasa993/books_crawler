import requests
import logging

from settings import api_endpoint


logging.basicConfig(level=logging.INFO)


def handle_api_response(response: requests.Response, success_msg: str) -> None:
    """
    Handle API response dynamically.
    """
    if response.status_code == 201:
        logging.info(success_msg)
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
    response = requests.post(f"{api_endpoint}/authors/", data=author_data)
    handle_api_response(response, "Author created successfully.")
    return response.json().get('id')


def fill_books(
    author_id: int,
    book_type_id: int,
    link: str,
    book_name: str
) -> None:
    """
    Fill db with books.
    """
    book_data = {
        "author": author_id,
        "book_type": book_type_id,
        "link": link,
        "name": book_name,
    }
    response = requests.post(f"{api_endpoint}/books/", data=book_data)
    handle_api_response(response, "Book created successfully.")


def fill_db(books_list: dict, book_type: int) -> None:
    """
    todo
    """
    for book in books_list.values():
        author_id = fill_authors(book['author'])
        fill_books(author_id, book_type, book['link'], book['title'])
