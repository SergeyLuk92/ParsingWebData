import asyncio
import httpx
import time

from src.parser import process_response, save_csv
from typing import List

time_start: float = time.time()
url: str = 'https://www.bazarok.ua/ru/'
num_pages: int = 5


async def process_request(request: httpx.Request):
    print(f'Отправил запрос {request.method} на хост {request.url}')


async def do_request(page: int):
    retries = 3
    for attempt in range(retries):
        async with httpx.AsyncClient(follow_redirects=True,
                                     event_hooks={'request': [process_request],
                                                  'response': [process_response]}) as client:
            res: httpx.Response = await client.get(url=(url + '?page=' + str(page)), follow_redirects=True)
            if res.status_code != 200:
                continue
            else:
                return print(res.status_code)


async def main():
    tasks: List = []
    for page in range(1, num_pages + 1):
        tasks.append(do_request(page))
    await asyncio.gather(*tasks)
    save_csv()


asyncio.run(main())
time_finish: float = time.time() - time_start
print(time_finish)
