import bs4.element

from parsers.price_collector import Parser


class KNSParser(Parser):
    def parse(self) -> dict:
        try:
            parse_result = list(map(lambda tag: tag['content'],
                                    filter(
                                        lambda t: t.name == 'meta' and (t['itemprop'] == "url" or t['itemprop'] == "price"),
                                        super().parse()[0].contents[1].contents[1].contents[1].contents[1].contents)))
        except Exception as e:
            print("kns error: ", e)
            return self.__result_dict
        self.__result_dict["price"] = [int(parse_result[1])]
        self.__result_dict["link"] = [f"https://www.kns.ru{parse_result[0]}"]
        return self.__result_dict

    def _filter(self, tag: bs4.element.Tag) -> bool:
        if tag.has_attr('class'):
            if 'block-price' in tag['class']:
                return True
        return False

    def __init__(self, product_name: str):
        self.__result_dict = {"price": [], "link": []}
        super().__init__(domain=f"https://www.kns.ru/search.aspx?s_word=", product_name=product_name)