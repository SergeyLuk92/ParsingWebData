from csv import writer
from os import getenv, makedirs, path
from typing import List, Optional, Dict

from loguru import logger
from httpx import Response
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()


class WebSiteParser:
    def __init__(self):
        self.our_list: List[Dict[str, str]] = []
        self.new_dict: dict[str, str] = {}

    async def process_response(self, response: Response) -> None:
        logger.info(f'Sent request to host {response.url}')
        await response.aread()
        bs4: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        cards = bs4.find_all('a', class_='decoration-none')
        self.parse_data(cards)

    def parse_data(self, cards: List) -> Optional[List[Dict[str, str]]]:
        for card in cards:
            try:
                link: str = card['href']
                title: str = card.find('div', class_='bloc_title').text
            except (KeyError, AttributeError):
                continue
            if link and title:
                self.our_list.append({"Title": title, "Link": link})
        return self.our_list

    def save_csv(self) -> None:
        output_dir = getenv("output_dir", "./files")
        csv_filename = getenv("csv_file_name", "output_data_collection.csv")
        makedirs(output_dir, exist_ok=True)
        output_path = path.join(output_dir, csv_filename)
        with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
            csv_writer = writer(csvfile)
            csv_writer.writerow(["Title", "Link"])
            for data in self.our_list:
                csv_writer.writerow([data["Title"], data["Link"]])
        logger.info("Data successfully saved to CSV")
