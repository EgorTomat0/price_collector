import re

import bs4.element

from parsers.price_collector import Parser


class RegardParser(Parser):
    def parse(self):
        try:
            parsing_result = super().parse()
            print(parsing_result)
            prices = [int(parsing_result[i].string[:-2].replace(u'\xa0', '')) for i in range(1, len(parsing_result), 2)]
            links = ["https://www.regard.ru/product/" + parsing_result[i].string.split()[1] for i in
                     range(0, len(parsing_result), 2)]
        except Exception as e:
            print("regard error: ", e)
            return self.__result_dict
        self.__result_dict["price"] = prices
        self.__result_dict["link"] = links
        return self.__result_dict

    @staticmethod
    def _filter(tag: bs4.element.Tag):
        if (tag.name == 'span' or tag.name == 'p') and tag.string is not None:
            if (re.search(r"\d\s₽", tag.string) is not None or "ID:" in tag.string) and len(tag['class']) != 0:
                return True
        return False

    def __init__(self, product_name: str):
        self.__result_dict = {"price": [], "link": []}
        super().__init__(domain=f"https://www.regard.ru/catalog/?search=", product_name=product_name)

