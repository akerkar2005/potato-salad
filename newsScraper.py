import requests
from bs4 import BeautifulSoup
import sys

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }

stockTicker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
print("Retrieving news for " + stockTicker + '\n')

response = requests.get('https://finance.yahoo.com/quote/' + stockTicker + '/news', headers=headers)
parser = BeautifulSoup(response.text, 'html.parser')

articles = parser.select('a .yf-82qtw3')

articlesDict = {}
lastName = None
for article in articles:
    if article.name == 'h3': lastName = article.text
    else: articlesDict[lastName] = article.text

for key in articlesDict:
    print("ARTICLE TITLE: " + key)
    print("DESCRIPTION: " + articlesDict[key])
    print("------------------------------------------------------------------------")

