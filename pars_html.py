from typing import Final

from bs4 import BeautifulSoup, Tag
import re

BASE_URL: Final = "https://sunlight.net/"


class ShopItem:
    def __init__(self, description: str, link: str, item_id: str, new_price: float, old_price: float):
        self.item_id = item_id
        self.description = description
        self.link = link
        self.new_price = new_price
        self.old_price = old_price
        self.discount = self.calculate_discount()

    def calculate_discount(self):
        discount = ((self.old_price - self.new_price) / self.old_price )* 100
        return round(discount)

    def __str__(self):
        return f"{self.item_id}, new price: {self.new_price}, old price: {self.old_price}, discount: {self.discount}%, " \
               f"link: {self.link}"



def parse_item_id(raw_link: str) -> str:
    _, item_id_with_extension = raw_link.rsplit("/", 1)
    item_id, _ = item_id_with_extension.split(".")
    return item_id


def generate_full_link(raw_link: str) -> str:
    return BASE_URL + raw_link


def generate_shop_item(item_tag: Tag) -> ShopItem:
    raw_link = item_tag["href"]
    item_id = parse_item_id(raw_link)
    full_link = generate_full_link(raw_link)
    description = item_tag.text.strip()
    for parents in item_tag.parents:
        new_price = float(parents.attrs['data-analytics-price'])
        old_price = float(parents.attrs['data-analytics-base-price'])
        break
    shop_item = ShopItem(description=description, link=full_link, item_id=item_id,
                    new_price=new_price, old_price=old_price)

    return shop_item


def pars_page(page: str) -> list[ShopItem]:
    soup = BeautifulSoup(page, "html.parser")
    pars_response = soup.find_all('a', class_="cl-item-link js-cl-item-link js-cl-item-root-link")
    items_in_page = list()
    for item in pars_response:
        items_in_page.append(generate_shop_item(item))
    return items_in_page


if __name__ == '__main__':
    with open('test.html', 'r') as file:
        content = file.read()
    r = pars_page(content)

    for i in r:
        print(i)
