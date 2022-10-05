
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path


# fetching symbols and names from wikipedia to provide common base for all scrapers
def parse_index_wiki_page(index_selection):
    index_url_dict = {
        "Nasdaq100": "https://en.wikipedia.org/wiki/Nasdaq-100",
        "DowJones": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
        # "DAX": "https://www.onvista.de/index/einzelwerte/DAX-Index-20735",
        # "MDAX": "https://www.onvista.de/index/einzelwerte/MDAX-Index-323547"
    }
    index_page = requests.get(index_url_dict[index_selection])
    index_soup = BeautifulSoup(index_page.content, "html.parser")
    return index_soup


def get_stock_names_and_symbols(index_soup, index_selection):
    if index_selection == "DowJones":
        table = index_soup.find("table", id="constituents")
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
        df = df.drop(["Exchange", "Industry", "Date added", "Notes", "Index weighting"], axis=1)
        df = df.rename(columns={"Company": "name", "Symbol": "symbol"})
        all_names = df["name"].tolist()
        all_symbols = df["symbol"].tolist()
        return all_names, all_symbols
    elif index_selection == "Nasdaq100":
        table = index_soup.find("table", id="constituents")
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
        df = df.drop(["GICS Sector", "GICS Sub-Industry"], axis=1)
        df = df.rename(columns={"Company": "name", "Ticker": "symbol"})
        all_names = df["name"].tolist()
        all_symbols = df["symbol"].tolist()
        return all_names, all_symbols
    else:
        print("Error in get_stock_symbols")


def create_zacks_links(all_symbols):
    all_links = []
    for symbol in all_symbols:
        link = f"https://www.zacks.com/stock/quote/{symbol}"
        all_links.append(link)
    return all_links


def get_zacks_rank(all_links):
    all_ranks = []
    for stock_link in all_links:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        stock_page = requests.get(stock_link, headers=headers, timeout=10)
        stock_soup = BeautifulSoup(stock_page.content, "html.parser")
        stock_rankbox = stock_soup.find("div", class_="quote_rank_summary")
        stock_rank = stock_rankbox.find("p", class_="rank_view").text.replace(" ", "")[1]
        all_ranks.append(stock_rank)
    return all_ranks


def create_data_frame(all_symbols, all_names, all_ranks):
    df = pd.DataFrame(list(zip(all_symbols, all_names, all_ranks)),
                      columns=["symbol", "name", f"ZacksRank_{time.strftime('%Y-%m-%d')}"])
    df = df.sort_values(f"ZacksRank_{time.strftime('%Y-%m-%d')}", ascending=True)
    return df


def write_df_to_csv(df, index_selection):
    if not Path(f"{index_selection}.csv").exists():
        df.to_csv(f"{index_selection}.csv", sep=';', index=False)
    elif Path(f"{index_selection}.csv").exists():
        df_old = pd.read_csv(f"{index_selection}.csv", sep=";")
        df = df.drop(["symbol"], axis=1)
        df = pd.merge(df_old, df, on='name')
        df.to_csv(f"{index_selection}.csv", sep=';', index=False)


def scrape_zacks(index_selection):
    index_soup = parse_index_wiki_page(index_selection)
    all_names, all_symbols = get_stock_names_and_symbols(index_soup, index_selection)
    all_links = create_zacks_links(all_symbols)
    all_ranks = get_zacks_rank(all_links)
    df = create_data_frame(all_symbols, all_names, all_ranks)
    write_df_to_csv(df, index_selection)
    return df


index_selection = input("Enter Index: 'Nasdaq100', 'DowJones'> ")
scrape_zacks(index_selection)
