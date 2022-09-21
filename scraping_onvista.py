
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = ("https://www.onvista.de/index/einzelwerte/DAX-Index-20735")
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# getting all links of a stock index
all_urls = []
for single_stock in soup.findAll("a", class_="link link--secondary text-size--medium text-weight--bold"):
    link_short = single_stock.get("href")
    link = f"https://www.onvista.de{link_short}"
    all_urls.append(link)

stars = []
for stock in all_urls:
    stock_page = requests.get(stock)
    stock_soup = BeautifulSoup(stock_page.content, "html.parser")
    stock_box = stock_soup.find("div", class_="col col-12 inner-spacing--none-top inner-spacing--none-bottom")
    stock_stars = stock_box.find_all("span", class_="icon icon--SvgCdStarFull16 icon--size-16 outer-spacing--xxsmall-left color--cd-black-21")
    stars.append(abs(len(stock_stars)-4))

names = []
for url in all_urls:
    url = url.replace("https://www.onvista.de/aktien/", "")
    url = url.replace("-Aktie-", "")
    name = url[0:-12]
    names.append(name)

df = pd.DataFrame(list(zip(names, stars)),
                  columns=["name", "TheScreener_stars"])
print(df)