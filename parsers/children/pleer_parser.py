import re

import bs4.element

from parsers.price_collector import Parser


class PleerParser(Parser):
    def parse(self):
        try:
            parsing_result = super().parse()
            prices = [int(t.string) for t in parsing_result if t['itemprop'] == "price"]
            links = ["https:"+t['content'] for t in parsing_result if t['itemprop'] == "url"]
        except Exception as e:
            print("pleer error: ", e)
            return self.__result_dict
        self.__result_dict["price"] = prices
        self.__result_dict["link"] = links
        return self.__result_dict

    @staticmethod
    def _filter(tag: bs4.element.Tag):
        if tag.name == "div" or tag.name == "meta":
            if tag.has_attr('itemprop'):
                if tag['itemprop'] == "url" or tag['itemprop'] == "price":
                    return True
        return False

    def __init__(self, product_name: str):
        self.__result_dict = {"price": [], "link": []}
        super().__init__(domain="https://www.pleer.ru/search_", product_name=product_name + '.html')
