import asyncio
import httpx
import time

from src.core.parser import WebSiteParser
from loguru import logger
from typing import List


class WebSiteCrawler:
    def __init__(self):
        self.url: str = 'https://www.bazarok.ua/ru/'
        self.num_pages: int = 5
        self.parser = WebSiteParser()

    async def process_request(self, request: httpx.Request) -> None:
        logger.info(f'Sent request  {request.method} to host {request.url}')

    async def do_request(self, page: int) -> None:
        retries = 3
        for attempt in range(retries):
            async with httpx.AsyncClient(follow_redirects=True,
                                         event_hooks={'request': [self.process_request],
                                                      'response': [self.parser.process_response]}) as client:
                res: httpx.Response = await client.get(url=(self.url + '?page=' + str(page)), follow_redirects=True)
                if res.status_code != 200:
                    continue
                else:
                    return logger.info(res.status_code)

    async def main(self) -> None:
        time_start: float = time.time()
        tasks: List = []
        for page in range(1, self.num_pages + 1):
            tasks.append(self.do_request(page))
        await asyncio.gather(*tasks)
        self.parser.save_csv()

        time_finish: float = time.time() - time_start
        logger.info(time_finish)
