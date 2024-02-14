import os
import threading

import util
import requests
from bs4 import BeautifulSoup

base_url = "https://www.crucial.com/upgrades"

space_man_map = {
    "A Open": "aopen",
    "BCM Advanced Research": "bcmadvancedresearch",
    "BFG Tech": "bfgtech",
    "Diamond Flower (DFI)": "diamondflower(dfi)",
    "Elite Group (ECS)": "elitegroup(ecs)",
    "HP - Compaq": "hp-compaq",
    "LG Electronics": "lgelectronics",
    "MSI (Micro Star)": "msi(microstar)",
    "Packard Bell": "packardbell",
    "PC Chips": "pcchips",
    "VIA Technologies": "viatechnologies",
    "Western Digital": "westerndigital"
}


def get_products(soup):
    products = []
    for a in soup.find_all("a", class_="element_item"):
        product = a.text
        products.append(product)
    return products


def scrape_man(url, man):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = get_products(soup)
    print(man)
    util.save_to_file(products, f"products/{man}_products.txt")


os.mkdir("products")
mans = util.read_file("manufacturers.txt")
for man in mans:
    if man in space_man_map:
        man = space_man_map[man]
    url = base_url + "/" + man
    threading.Thread(target=scrape_man, args=(url, man,)).start()

