import asyncio
import httpx
import time
import csv
from bs4 import BeautifulSoup
from typing import List

time_start: float = time.time()
url: str = 'https://www.bazarok.ua/ru/'
num_pages: int = 5


async def process_request(request: httpx.Request):
    print(f'Отправил запрос {request.method} на хост {request.url}')


async def process_response(response: httpx.Response):
    print(f'Отправил запрос на хост {response.url}')
    await response.aread()
    bs4: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
    cards = bs4.find_all('a', class_='decoration-none')
    parse_data(cards)


def parse_data(cards: List):
    global our_list
    for card in cards:
        try:
            link: str = card['href']
            title: str = card.find('div', class_='bloc_title').text
        except KeyError:
            continue
        if link and title:
            our_list.append([(title, link)])


async def do_request(page: int):
    async with httpx.AsyncClient(follow_redirects=True,
                                 event_hooks={'request': [process_request], 'response': [process_response]}) as client:
        res: httpx.Response = await client.get(url=(url + '?page=' + str(page)), follow_redirects=True)
        if res.status_code != 200:
            return await do_request(page)
        print(res.status_code)


async def main():
    tasks: List = []
    for page in range(1, num_pages):
        tasks.append(do_request(page))
    await asyncio.gather(*tasks)


our_list: List = []
new_dict: dict = {}
asyncio.run(main())
for data in our_list:
    new_dict.update(data)
with open('outputdatacollection.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer: csv.writer = csv.writer(csvfile)
    for key, value in new_dict.items():
        writer.writerow([key, value])
time_finish: float = time.time() - time_start
print(time_finish)
