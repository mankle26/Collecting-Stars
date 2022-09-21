# Collecting stars
*Practising web-scraping and for-loops in Python*

## The task
The website onvista.de provides various facts about stocks, 
including a TheScreener-Rating for the expected performance.
However, these ratings are not available as a list (e.g. for all 
DAX companies). They are only displayed on the page of each single stock.
I wanted to have these ratings next to the company´s name in a dataframe 
for easier comparison. 

## The solution
The program in this folder runs through all single stock pages
and fetches the stars of each of them. At the end, they are put together
with the names in a data frame.

Here an example output (20.09.22):

| name                          | Stars |
|-------------------------------|-------|
| Adidas                        | 1     |
| Airbus-Group-EADS             | 1     |
| Allianz                       | 3     |
| BASF                          | 2     |
| Bayer                         | 2     |
| BMW                           | 1     |
| Beiersdorf                    | 3     |
| Brenntag                      | 4     |
| Continental                   | 1     |
| Covestro                      | 1     |
| Daimler-Truck                 | 2     |
| Deutsche-Bank                 | 4     |
| Deutsche-Boerse               | 4     |
| Deutsche-Post                 | 1     |
| Deutsche-Telekom              | 4     |
| EON                           | 2     |
| Fresenius-Medical-Care        | 1     |
| Fresenius                     | 2     |
| Hannover-Rueck                | 4     |
| HeidelbergCement              | 1     |
| Henkel                        | 4     |
| Infineon                      | 2     |
| Linde                         | 1     |
| Mercedes-Benz-Group-Daimler   | 2     |
| Merck                         | 2     |
| MTU-Aero-Engines              | 2     |
| Muenchener-Rueck              | 4     |
| Porsche-Autmomobil-Holding-SE | 3     |
| Puma                          | 1     |
| QIAGEN-NV                     | 4     |
| RWE                           | 3     |
| SAP                           | 1     |
| Satorius-AG                   | 1     |
| Siemens                       | 2     |
| Siemens-Energy                | 1     |
| Siemens-Healthineers          | 2     |
| Symrise                       | 1     |
| Volkswagen-VZ                 | 4     |
| Vonovia                       | 2     |
| Zalando                       | 1     |

