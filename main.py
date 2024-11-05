"""
This module contains functions to scrape book data from books.toscrape.com.

It includes the `scrape_books` function to fetch book details from multiple pages
and the `main` function to execute the scraping process.
"""

import time
import requests
from bs4 import BeautifulSoup


def scrape_books(
    base_url: str,
    start_page: int,
    end_page: int,
    sleep_time: int = 1,
    timeout: int = 10
) -> list[dict[str, str]]:
    """
    Scrapes book data from the specified range of pages on the given base URL.

    Args:
        base_url (str): The base URL of the book catalog.
        start_page (int): The starting page number for scraping.
        end_page (int): The ending page number for scraping.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing book details
                              (title, price, availability).
    """

    book_data = []

    for page_num in range(start_page, end_page):
        url = f"{base_url}page-{str(page_num)}.html"

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Error fetching page {page_num}: {error}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        book_entries = soup.find_all("article", class_="product_pod")

        for entry in book_entries:
            book = {
                "title": entry.h3.a["title"],
                "price": entry.find("p", class_="price_color").text.strip(),
                "availability": entry.find("p", class_="instock availability").text.strip()
            }
            book_data.append(book)

        print(f"Processed page {page_num} of {end_page}.")
        time.sleep(sleep_time)

    return book_data

def main():
    """
    Main function to initiate the book scraping process and print the results.

    This function sets the base URL, calls the scrape_books function,
    and prints each book's details.
    """

    base_url = "https://books.toscrape.com/catalogue/"
    book_data = scrape_books(base_url, start_page=1, end_page=50)

    for book in book_data:
        print(book)

if __name__ == "__main__":
    main()
