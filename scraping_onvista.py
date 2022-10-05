import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path


def parse_index_page(index_selection):
    index_url_dict = {
        "Nasdaq100": "https://www.onvista.de/index/einzelwerte/NASDAQ-100-Index-325104",
        "DowJones": "https://www.onvista.de/index/einzelwerte/Dow-Jones-Index-324977",
        "DAX": "https://www.onvista.de/index/einzelwerte/DAX-Index-20735",
        "MDAX": "https://www.onvista.de/index/einzelwerte/MDAX-Index-323547"
    }
    index_page = requests.get(index_url_dict[index_selection])
    index_soup = BeautifulSoup(index_page.content, "html.parser")
    return index_soup


def get_stock_urls(soup):
    all_urls = []
    for single_stock in soup.findAll("a", class_="link link--secondary text-size--medium text-weight--bold"):
        link_short = single_stock.get("href")
        link = f"https://www.onvista.de{link_short}"
        all_urls.append(link)
    return all_urls


def get_stock_stars(all_urls):
    all_stars = []
    for stock in all_urls:
        stock_page = requests.get(stock)
        stock_soup = BeautifulSoup(stock_page.content, "html.parser")
        stock_box = stock_soup.find("div", class_="col col-12 inner-spacing--none-top inner-spacing--none-bottom")
        # check if it has at least one star
        stock_first_star = len(stock_box.findAll("span", class_="icon icon--SvgCdStarFull16 icon--size-16"))
        if stock_first_star == 1:  # check for more stars
            stock_more_stars = stock_box.findAll("span",
                                                 class_="icon icon--SvgCdStarFull16 icon--size-16 "
                                                        "outer-spacing--xxsmall-left")
            all_stars.append(len(stock_more_stars) + stock_first_star)
        else:
            all_stars.append(0)
    return all_stars


def get_stock_names_and_symbols(index_selection):
    if index_selection == "DowJones":
        index_page = requests.get("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average")
        index_soup = BeautifulSoup(index_page.content, "html.parser")
        table = index_soup.find("table", id="constituents")
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
        df = df.drop(["Exchange", "Industry", "Date added", "Notes", "Index weighting"], axis=1)
        df = df.rename(columns={"Company": "name", "Symbol": "symbol"})
        all_names = df["name"].tolist()
        all_symbols = df["symbol"].tolist()
        return all_names, all_symbols
    elif index_selection == "Nasdaq100":
        index_page = requests.get("https://en.wikipedia.org/wiki/Nasdaq-100")
        index_soup = BeautifulSoup(index_page.content, "html.parser")
        table = index_soup.find("table", id="constituents")
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
        df = df.drop(["GICS Sector", "GICS Sub-Industry"], axis=1)
        df = df.rename(columns={"Company": "name", "Ticker": "symbol"})
        all_names = df["name"].tolist()
        all_symbols = df["symbol"].tolist()
        return all_names, all_symbols
    elif index_selection == "DAX":
        index_page = requests.get("https://de.wikipedia.org/wiki/DAX")
        index_soup = BeautifulSoup(index_page.content, "html.parser")
        table = index_soup.find("table", id="zusammensetzung")
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
        df = df.rename(columns={"Name": "name", "Symbol": "symbol"})
        all_names = df["name"].tolist()
        all_symbols = df["symbol"].tolist()
        return all_names, all_symbols
    elif index_selection == "MDAX":
        index_page = requests.get("https://en.wikipedia.org/wiki/MDAX")
        index_soup = BeautifulSoup(index_page.content, "html.parser")
        table = index_soup.find("table", id="constituents")
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
        df = df.rename(columns={"Name": "name", "Symbol": "symbol"})
        all_names = df["name"].tolist()
        all_symbols = df["symbol"].tolist()
        return all_names, all_symbols
    else:
        print("Error in get_stock_symbols")


def create_data_frame(all_symbols, all_names, all_stars):
    df = pd.DataFrame(list(zip(all_symbols, all_names, all_stars)),
                      columns=["symbol", "name", f"TheScreener_{time.strftime('%Y-%m-%d')}"])
    df = df.sort_values(f"TheScreener_{time.strftime('%Y-%m-%d')}", ascending=False)
    return df


def write_df_to_csv(df, index_selection):
    if not Path(f"{index_selection}.csv").exists():
        df.to_csv(f"{index_selection}.csv", sep=';', index=False)
    elif Path(f"{index_selection}.csv").exists():
        df_old = pd.read_csv(f"{index_selection}.csv", sep=";")
        df = df.drop(["symbol"], axis=1)
        df = pd.merge(df_old, df, on='name')
        df.to_csv(f"{index_selection}.csv", sep=';', index=False)


def scrape_onvista(index_selection):
    index_soup = parse_index_page(index_selection)
    stock_urls = get_stock_urls(index_soup)
    all_stars = get_stock_stars(stock_urls)
    all_names, all_symbols = get_stock_names_and_symbols(index_selection)
    df = create_data_frame(all_symbols, all_names, all_stars)
    write_df_to_csv(df, index_selection)


index_selection = input("Enter Index: 'Nasdaq100', 'DowJones', 'DAX', 'MDAX'> ")
pd.DataFrame(scrape_onvista(index_selection))

# df.to_csv(f"{index_selection}.csv", sep=';', index=False)

