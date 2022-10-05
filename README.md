# Stocks scrapers
*Practising web-scraping in Python*

## The task
The website onvista.de provides various facts about stocks, 
including a TheScreener-Rating for the expected performance.
However, these ratings are not available as a list (e.g. for all 
DAX companies). They are only displayed on the page of each single stock.

Similar, Zacks.com offers a so-called "Zacks Rank" summarizing their
evaluation of the respective stock. Just like onvista, these are
openly available for each stock at its related page but not as a list.

I wanted to have these ratings next to the company´s name in a dataframe 
for easier comparison. 

## The solution
The program in this folder runs through all single stock pages of an index
and fetches the ratings for each of them. At the end, they are put together
with the names and symbols of each stock in a data frame.

Here an example output (05.10.22):

| symbol | name                     | TheScreener | Zacks |
|--------|--------------------------|-------------|-------|
| WMT    | Walmart                  | 2           | 2     |
| AXP    | American Express         | 2           | 2     |
| V      | Visa                     | 3           | 2     |
| JPM    | JPMorgan Chase           | 1           | 2     |
| VZ     | Verizon                  | 1           | 3     |
| UNH    | UnitedHealth             | 2           | 3     |
| TRV    | Travelers                | 3           | 3     |
| CRM    | Salesforce               | 3           | 3     |
| PG     | Procter & Gamble         | 3           | 3     |
| MSFT   | Microsoft                | 1           | 3     |
| MRK    | Merck                    | 1           | 3     |
| MCD    | McDonald's               | 2           | 3     |
| JNJ    | Johnson & Johnson        | 2           | 3     |
| MMM    | 3M                       | 2           | 3     |
| HD     | Home Depot               | 2           | 3     |
| DIS    | Disney                   | 1           | 3     |
| KO     | Coca-Cola                | 2           | 3     |
| CSCO   | Cisco                    | 2           | 3     |
| CVX    | Chevron                  | 1           | 3     |
| CAT    | Caterpillar              | 2           | 3     |
| AAPL   | Apple                    | 1           | 3     |
| AMGN   | Amgen                    | 2           | 3     |
| HON    | Honeywell                | 1           | 3     |
| WBA    | Walgreens Boots Alliance | 2           | 4     |
| GS     | Goldman Sachs            | 3           | 4     |
| NKE    | Nike                     | 2           | 4     |
| BA     | Boeing                   | 2           | 4     |
| IBM    | IBM                      | 2           | 4     |
| INTC   | Intel                    | 2           | 5     |
| DOW    | Dow                      | 2           | 5     |
