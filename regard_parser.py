import re

import bs4.element

from price_collector import Parser


class RegardParse(Parser):
    def parse(self):
        pass

    @staticmethod
    def _filter(tag: bs4.element.Tag):
        pass

    def __init__(self, domain: str, product_name: str):
        super().__init__(domain=domain)
