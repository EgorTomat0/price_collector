import re

import bs4.element

from price_collector import Parser


class PleerParser(Parser):
    def parse(self):
        parsing_result = ' '.join(map(lambda html_tag: str(html_tag), super().parse()))
        prices = list(map(lambda p: int(p[1:-1]), list(dict.fromkeys(re.findall(r'>\d+<', parsing_result)))))
        links = list(map(lambda l: f"https://www.pleer.ru/{l}",
                         list(dict.fromkeys(re.findall(r"/product\S+html", parsing_result)))))
        self.__result_dict["price"] = prices
        self.__result_dict["link"] = links
        return self.__result_dict

    def _filter(self, tag: bs4.element.Tag):
        if tag.name == 'div' and super()._filter(tag):
            html_in_string = ' '.join(map(lambda html_tag: str(html_tag), tag.contents))
            if re.search(r'\d+', html_in_string) is not None and 'onclick' in html_in_string:
                return True
        return False

    def __init__(self, product_name: str):
        self.__result_dict = {"price": [], "link": []}
        super().__init__(domain="https://www.pleer.ru/search_", product_name=product_name + '.html')
