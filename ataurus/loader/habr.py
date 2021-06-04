import numpy as np
import requests
import bs4
import logging
import asyncio
import random
import pandas as pd
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
        self._limit_incorrect = 20

    async def parse_by_authors(self, authors: list[str], max_count=None) -> pd.DataFrame:
        """
        Gets articles from Habr.com by the authors' names.

        :param authors: the names of authors
        :param max_count: the maximum count of articles per an author
        :return: a DataFrame object containing the 'post_number', 'author' and 'text' columns
        """
        # Run a timer
        logging.warning("Parsing beginning...")
        begin_time = datetime.now()

        tasks = []
        for sublist_authors in get_sublists(authors, self._concurrent):
            tasks.append(self._get_links_by_authors(sublist_authors, max_count))
        links = np.hstack(await asyncio.gather(*tasks)).tolist()

        tasks = []
        for sublist_links in get_sublists(links, self._concurrent):
            tasks.append(self._parse(sublist_links))
        values = np.vstack(await asyncio.gather(*tasks))

        dataframe = pd.DataFrame(np.vstack(values), columns=['post_number', 'author', 'text'])

        # Stop the timer
        logging.warning('Parsing was completed')
        logging.warning(f'Work time: {datetime.now() - begin_time}')

        return dataframe

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

    async def _parse(self, links: list[str]) -> np.ndarray:
        """
        Parses web sites and returns a list of values representing 'post_number', 'author' and 'text' columns.

        :param links: a list of links that must be parsed
        :return: numpy.ndarray containing post_number', 'author' and 'text' values for the each link
        """
        # A counter of incorrect requests
        incorrect_count = 0
        # A list of finish values
        values = []

        for link in links:
            post_number = link.split('/')[-2]

            response = requests.get(link)

            if response.status_code == 200:
                # Reset the counter
                # If the counter becomes equal to self._limit_incorrect, parsing ends
                incorrect_count = 0

                # The count of correct parsed posts
                self._count += 1

                bs = bs4.BeautifulSoup(response.text, features='html.parser')
                author = bs.find(class_=self.USERNAME_CLASS).text
                title = bs.find(class_=self.TITLE_CLASS).text
                text = bs.find(class_=self.TEXT_CLASS).text

                logging.warning(f"(#{self._count}) id={post_number} {author}: {title}")

                values.append((post_number, author, text))

            elif response.status_code == 404:
                logging.warning(f"(#{self._count}) id={post_number} Error 404")

                # Increase the counter of incorrect requests
                incorrect_count += 1

                if incorrect_count == self._limit_incorrect:
                    break
            else:
                logging.warning(f"(#{self._count}) id={post_number} Error {response.status_code}")

            # Take the timeout to avoid a ban
            await asyncio.sleep(self._timeout + random.randint(0, 5) * random.random())

        return np.vstack(values)
