import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path
# import re


class Index:
    def __init__(self, name):
        self.name = name
        index_url_dict = {
            "Nasdaq100": "https://en.wikipedia.org/wiki/Nasdaq-100",
            "DowJones": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
            # "DAX": "https://de.wikipedia.org/wiki/DAX",
            # "MDAX": "https://de.wikipedia.org/wiki/MDAX"
        }
        index_page = requests.get(index_url_dict[self.name])
        index_soup = BeautifulSoup(index_page.content, "html.parser")
        # if name == "Nasdaq100" or "DowJones":
        table = index_soup.find("table", id="constituents")
        # elif name == "DAX" or "MDAX":
        # table = index_soup.find("table", id="zusammensetzung")
        df = pd.DataFrame(pd.read_html(str(table))[0])
        df.columns = df.columns.str.lower()
        df_names = df.filter(regex=r"(name|company)")
        df_symbols = df.filter(regex=r"(symbol|ticker)")
        self.names = df_names.iloc[:, 0].tolist()
        self.symbols = df_symbols.iloc[:, 0].tolist()
        self.zacks_ranks = []
        self.screener_stars = []
        self.df = pd.DataFrame()

    def get_zacks_ranks(self):
        all_zacks_links = []
        for symbol in self.symbols:
            link = f"https://www.zacks.com/stock/quote/{symbol}"
            all_zacks_links.append(link)
        all_zacks_ranks = []
        for single_zacks_link in all_zacks_links:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            stock_page = requests.get(single_zacks_link, headers=headers, timeout=10)
            stock_soup = BeautifulSoup(stock_page.content, "html.parser")
            stock_rankbox = stock_soup.find("div", class_="quote_rank_summary")
            stock_rank = stock_rankbox.find("p", class_="rank_view").text.replace(" ", "")[1]
            all_zacks_ranks.append(stock_rank)
        self.zacks_ranks = all_zacks_ranks
        return all_zacks_ranks

    def get_screener_stars(self):
        onvista_url_dict = {
            "Nasdaq100": "https://www.onvista.de/index/einzelwerte/NASDAQ-100-Index-325104",
            "DowJones": "https://www.onvista.de/index/einzelwerte/Dow-Jones-Index-324977",
            "DAX": "https://www.onvista.de/index/einzelwerte/DAX-Index-20735",
            "MDAX": "https://www.onvista.de/index/einzelwerte/MDAX-Index-323547"
        }
        index_page = requests.get(onvista_url_dict[self.name])
        index_soup = BeautifulSoup(index_page.content, "html.parser")
        all_urls = []
        for single_stock in index_soup.findAll("a", class_="link link--secondary text-size--medium text-weight--bold"):
            link_short = single_stock.get("href")
            link = f"https://www.onvista.de{link_short}"
            all_urls.append(link)
        all_stars = []
        for stock in all_urls:
            stock_page = requests.get(stock)
            stock_soup = BeautifulSoup(stock_page.content, "html.parser")
            stock_box = stock_soup.find("div",
                                        class_="col col-12 inner-spacing--none-top inner-spacing--none-bottom")
            # check if it has at least one star
            stock_first_star = len(stock_box.findAll("span", class_="icon icon--SvgCdStarFull16 icon--size-16"))
            if stock_first_star == 1:  # check for more stars
                stock_more_stars = stock_box.findAll("span",
                                                     class_="icon icon--SvgCdStarFull16 icon--size-16 "
                                                            "outer-spacing--xxsmall-left")
                all_stars.append(len(stock_more_stars) + stock_first_star)
            else:
                all_stars.append(0)
        self.screener_stars = all_stars
        return all_stars

    def compile_df(self):
        df = pd.DataFrame(list(zip(self.symbols, self.names, self.zacks_ranks, self.screener_stars)),
                          columns=["symbol", "name", f"ZacksRank_{time.strftime('%Y-%m-%d')}", f"ScreenerStars_{time.strftime('%Y-%m-%d')}"])
        df = df.sort_values(f"ZacksRank_{time.strftime('%Y-%m-%d')}", ascending=True)
        self.df = df
        return df

    def write_df_to_csv(self):
        if not Path(f"{self.name}.csv").exists():
            self.df.to_csv(f"{self.name}.csv", sep=';', index=False)
            print(f"New file {self.name}.csv has been created in folder.")
        elif Path(f"{self.name}.csv").exists():
            df_old = pd.read_csv(f"{self.name}.csv", sep=";")
            df = self.df.drop(["name"], axis=1)
            df = pd.merge(df_old, df, on='symbol')
            df.to_csv(f"{self.name}.csv", sep=';', index=False)
            print(f"New data has been appended to {self.name}.csv")
        return self.df


dow = Index("Nasdaq100")

print(dow.symbols)
print(dow.get_zacks_ranks())
print(dow.get_screener_stars())
print(dow.compile_df())
dow.write_df_to_csv()
