#!/usr/bin/env python3

import urllib.request
import re

from database import Database
from product import Product

def fetch_list_page(page):
    base_url = ("https://ingatlan.com/szukites/kiado+lakas+budapest+havi-140000-ezer-Ft-ig?page=%d" % (page))
    with urllib.request.urlopen(base_url) as response:
        return response.read().decode("utf-8")

def parse_product_pages(html):
    return re.findall(r"class=\"listing[^>]*data-id=\"(\d+)\"", html)

def fetch_product_page(product_id):
    base_url = ("https://ingatlan.com/%s" % (product_id))
    with urllib.request.urlopen(base_url) as response:
        return response.read().decode("utf-8")

db = Database()

for page in list(range(1, 20)):
    print(" -- Page #{:0>2}".format(page))
    list_page = fetch_list_page(page)
    product_ids = set(parse_product_pages(list_page))

    added = 0
    for product_id in product_ids:
        if db.is_exists("properties", "id", product_id):
            continue
        product_page = fetch_product_page(product_id)
        product = Product.parse(product_page, product_id)
        print("  - Add {}".format(product.data['id']))
        db.insert("properties", product)
        added += 1
    if added < 1:
        print("No more new properties on this page. Stop parsing.")
        break
