import os
import threading

import util
import requests
from bs4 import BeautifulSoup

base_url = "https://www.crucial.com/upgrades"


def get_models(soup):
    products = []
    for a in soup.find_all("a", class_="element_item"):
        model = a.text
        if "href" not in a.attrs:
            continue
        link = a["href"]
        products.append(f"{model},{link}")
    return products


def scrape_product(url, full_product_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(full_product_name)
    models = get_models(soup)
    if len(models) > 0:
        util.save_to_file(models, f"models/{full_product_name}")


os.chdir("products")
mans_files = [man_f for man_f in os.listdir() if man_f.endswith("_products.txt")]
os.chdir("..")
os.makedirs("models")
for man_f in mans_files:
    print(man_f)
    man_products = util.read_file(f'products/{man_f}')
    man_url = base_url + "/" + man_f.split("_")[0].replace(' ', '-') + "/"
    for product in man_products:
        product_name = product.replace(" ", "-").replace("/", "-").replace("\\", "-").replace(".", "*")
        url = man_url + product_name
        full_product_name = man_f.split("_")[0] + "_" + product_name
        threading.Thread(target=scrape_product, args=(url, full_product_name)).start()
