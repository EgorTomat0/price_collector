from abc import ABC, abstractmethod

import bs4
import requests

HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}


class Parser(ABC):
    @abstractmethod
    def parse(self):
        parsing_result = bs4.BeautifulSoup(self._init_request.text, 'lxml').find_all(self._filter)
        return parsing_result

    @staticmethod
    @abstractmethod
    def _filter(tag: bs4.element.Tag):
        if tag.has_attr('class'):
            if "price" in ' '.join(tag['class']):
                return True
        return False

    @abstractmethod
    def __init__(self, domain: str, product_name: str):
        self._init_request = requests.get(f'{domain}{product_name.replace(" ", "+")}', headers=HEADERS)
