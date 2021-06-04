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


class Parser:
    URL = "https://habr.com/ru/post/{post_number}"
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

    async def parse(self,
                    count: int = None,
                    min_post: int = 1,
                    max_post: int = 1000000):
        """
        Method parses the posts from habr.com and inserts them as documents in the Elasticsearch cluster.

        :param count: the count of posts that will be inserted in the index
        :param min_post: the number of the first post to be parsed from
        :param max_post: the number of the post to which the parsing will be performed
        """
        # Run a timer
        logging.warning("Parsing beginning...")
        begin_time = datetime.now()

        sublists = get_sublists(list(range(min_post, max_post + 1)), self._concurrent)
        tasks = []
        for sublist in sublists:
            tasks.append(self._parse(sublist, count))
        await asyncio.gather(*tasks)

        logging.warning('Parsing was completed')
        logging.warning(f'Work time: {datetime.now() - begin_time}')


    async def _parse(self, post_numbers: list[int], count: int):
        incorrect_count = 0

        for post_number in post_numbers:
            if count and self._count >= count:
                break

            url = self.URL.format(post_number=post_number)
            response = requests.get(url)

            if response.status_code == 200:
                # Reset the counter
                # If the counter becomes equal to self._limit_incorrect, parsing ends
                incorrect_count = 0

                # The count of correct parsed posts
                self._count += 1

                bs = bs4.BeautifulSoup(response.text, features='html.parser')
                author = bs.find(class_=self.USERNAME_CLASS).text
                post_date = bs.find(class_=self.DATETIME_CLASS).get(self.DATETIME_KEY)
                title = bs.find(class_=self.TITLE_CLASS).text
                text = bs.find(class_=self.TEXT_CLASS).text

                logging.warning(f"(#{self._count}) id={post_number} {author}: {title}")

                self._database.add(post_number, author, text, title, post_date)
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
