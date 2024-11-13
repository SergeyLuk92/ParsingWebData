import csv
import httpx
from typing import List
from bs4 import BeautifulSoup

our_list: List = []
new_dict: dict[str, str] = {}


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
    if our_list:
        return our_list


def save_csv():
    for data in our_list:
        new_dict.update(data)
    with open('output_data_collection.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer: csv.writer = csv.writer(csvfile)
        for key, value in new_dict.items():
            writer.writerow([key, value])
