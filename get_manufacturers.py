import util
import requests
from bs4 import BeautifulSoup

url = "https://www.crucial.com/upgrades"
response = requests.get(url)


def get_manufacturers(soup):
	manufacturers = []
	for a in soup.find_all("a", class_="element_item"):
		manufacturer = a.text
		manufacturers.append(manufacturer)
	return manufacturers


if response.ok:
	soup = BeautifulSoup(response.text, "html.parser")
	mans = get_manufacturers(soup)
	util.save_to_file(mans, "manufacturers.txt")
