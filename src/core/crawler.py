from time import time
from asyncio import gather
from typing import List, Coroutine

from loguru import logger
from httpx import Response, AsyncClient, Request

from src.core.parser import WebSiteParser


class WebSiteCrawler:
    def __init__(self):
        self.url: str = 'https://www.bazarok.ua/ru/'
        self.num_pages: int = 5
        self.parser = WebSiteParser()

    async def process_request(self, request: Request) -> None:
        logger.info(f'Sent request  {request.method} to host {request.url}')

    async def do_request(self, page: int) -> None:
        retries = 3
        for attempt in range(retries):
            async with AsyncClient(follow_redirects=True,
                                   event_hooks={'request': [self.process_request],
                                                'response': [self.parser.process_response]}) as client:
                res: Response = await client.get(url=(self.url + '?page=' + str(page)), follow_redirects=True)
                if res.status_code != 200:
                    continue
                else:
                    return logger.info(res.status_code)

    async def main(self) -> None:
        time_start: float = time()
        tasks: List[Coroutine] = [self.do_request(page) for page in range(1, self.num_pages + 1)]
        await gather(*tasks)
        self.parser.save_csv()
        time_finish: float = time() - time_start
        logger.info(time_finish)
