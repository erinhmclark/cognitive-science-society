""" Scraper for the Cognitive Science Society.
    https://cognitivesciencesociety.org/blog/
"""
import datetime as dt
import logging
from typing import Optional, Dict, Any, List
import mysql.connector
from mysql.connector.connection import MySQLConnection
import requests
from uuid import uuid4
from bs4 import BeautifulSoup
from ratelimit import limits
from settings import (BASE_URL,
                      PAGE_LIMIT,
                      COG_SS_TABLE,
                      MYSQL_CONFIG)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_older_posts(soup: BeautifulSoup) -> Optional[str]:
    """
    Returns URL of the older posts page if exists, otherwise None.

    Args:
        soup (BeautifulSoup): Soup object for the current page.

    Returns:
        Optional[str]: URL of the older posts page or None
    """
    try:
        return soup.find('a', string='« Older Entries')['href']
    except AttributeError:
        logger.exception("Failed to fetch URL of older posts page.", exc_info=True)
        return None


@limits(calls=100, period=300)
def get_soup(url: str) -> BeautifulSoup:
    """
    Returns a BeautifulSoup object for a given URL.

    Args:
        url (str): URL to scrape.

    Returns:
        BeautifulSoup: BeautifulSoup object for the provided URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def get_blog_posts(soup: BeautifulSoup) -> Optional[List[BeautifulSoup]]:
    """
    Returns a list of BeautifulSoup objects for each blog post on the page.

    Args:
        soup (BeautifulSoup): Soup object for the current page.

    Returns:
        Optional[List[BeautifulSoup]]: List of BeautifulSoup objects for each blog post.
    """
    try:
        return soup.find('div', {'class': 'et_pb_salvattore_content'}).find_all('article')
    except AttributeError:
        logger.exception("Failed to fetch list of blog posts.")
        return None


def convert_date(date_string: str, date_format: str) -> dt.date:
    """
    Converts a date string into a datetime object, adding zero padding to days.

    Args:
        date_string (str): Date string to convert.
        date_format (str): Date format to convert the string to.

    Returns:
        datetime.date: Converted date object.
    """
    month, day, year = date_string.split()
    if len(day) == 2:
        date_string = f'{month} 0{day} {year}'
    return dt.datetime.strptime(date_string, date_format).date()


def get_blog_details(post: BeautifulSoup) -> Dict[str, Any]:
    """
    Returns a dictionary with blog details from a BeautifulSoup post object.

    Args:
        post (BeautifulSoup): Soup object of a blog post.

    Returns:
        Dict[str, Any]: Dictionary containing blog details.
    """
    title = post.h2.text
    date_published = post.find('span', {'class': 'published'}).text
    date_published_clean = convert_date(date_published, '%b %d, %Y')
    link = post.h2.a['href']
    tags = [tag.text for tag in post.find('p', {'class': 'post-meta'}).findAll('a')]
    tags_string = ', '.join(tags)
    blog_soup = get_soup(link)
    full_text = blog_soup.find('div', {'class': 'et_pb_row et_pb_row_2_tb_body'}).text
    data = {
        'entry_id': str(uuid4()),
        'title': title,
        'date_published': date_published_clean,
        'link': link,
        'tags': tags_string,
        'full_text': full_text,
    }
    return data


def get_database_connection() -> MySQLConnection:
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Error: {e}")


def insert_into_database(blog_details: Dict[str, Any], conn: MySQLConnection) -> None:
    """
    Inserts one row of blog details into a MySQL database.

    Args:
        blog_details (Dict[str, Any]): Dictionary containing blog details.
        conn (MySQLConnection): Database connection object.
    """
    query = f"""
        INSERT INTO {COG_SS_TABLE} (entry_id, updated, title, date_published, link, tags, full_text) 
        VALUES (%(entry_id)s, NOW(), %(title)s, %(date_published)s, %(link)s, %(tags)s, %(full_text)s)
        AS new
        ON DUPLICATE KEY UPDATE 
            title = new.title, 
            date_published = new.date_published,
            link = new.link,
            tags = new.tags,
            full_text = new.full_text,
            updated = NOW()
    """

    with conn.cursor() as cursor:
        cursor.execute(query, blog_details)
        conn.commit()
        logger.info(f"Inserted/Updated blog post {blog_details['entry_id']} into the database.")


def scrape_css_blog(url: str) -> None:
    """
    Scrapes a Cognitive Science Society blog, extracting blog details.

    Args:
        url (str): URL of the blog to scrape.
    """
    for i in range(PAGE_LIMIT):
        soup = get_soup(url)
        blog_posts = get_blog_posts(soup)
        for blog in blog_posts:
            try:
                blog_details = get_blog_details(blog)
                with get_database_connection() as conn:
                    insert_into_database(blog_details, conn)
            except Exception as e:
                logger.exception("Failed to extract blog details and insert into the database:", exc_info=True)

        older_posts = get_older_posts(soup)
        if not older_posts:
            break


if __name__ == "__main__":
    scrape_css_blog(BASE_URL)
