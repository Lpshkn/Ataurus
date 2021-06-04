import requests
import bs4
import logging
import asyncio
import random
from database.client import Database
from loader.utils import get_sublists
from datetime import datetime

logging.basicConfig(format="[%(asctime)s] %(msg)s",
                    level=logging.WARNING)


class HabrParser:
    URL_POST = "https://habr.com/ru/post/{post_number}"
    URL_USER = "https://habr.com/ru/users/{username}/posts/page{page_number}"
    USERNAME_CLASS = "user-info__nickname user-info__nickname_small"
    DATETIME_CLASS = "post__time"
    DATETIME_KEY = "date-time_published"
    TITLE_CLASS = "post__title-text"
    TEXT_CLASS = "post__text"

    def __init__(self,
                 database: Database,
                 timeout: int = 3,
                 concurrent: int = 1):
        """
        :param database: the object of Database
        :param timeout: timeout to make request in seconds
        :param concurrent: count of concurrent tasks: it may be speed up the process of parsing
        """
        self._database = database
        self._timeout = timeout
        self._concurrent = concurrent

        # The count of processed and indexed posts
        self._count = 0

        # Count of incorrect consecutive requests
        # This case allows to determine the max id among all the posts from the site
        self._limit_incorrect = 15

    async def _get_links_by_authors(self, authors: list[str], max_count: int) -> list[str]:
        """
        Gets a list of links of Habr articles by the author's name.

        :param authors: a list of authors' names
        :param max_count: the maximum count of articles per an author
        :return: a list of links
        """
        if max_count is None:
            max_count = 10**10

        all_links = []
        for author in authors:
            author_links = []
            page_number = 1
            while True:
                url = self.URL_USER.format(username=author, page_number=page_number)
                response = requests.get(url)

                if response.status_code == 200:
                    bs = bs4.BeautifulSoup(response.text, features='html.parser')
                    links = [link.get('href') for link in bs.find_all('a', class_='post__title_link')]
                    if links:
                        author_links.extend(links)
                        if len(author_links) > max_count:
                            break
                    else:
                        break
                else:
                    break

                page_number += 1

            all_links.extend(author_links[:max_count])

        return all_links

