from stockScraper import StockScraper
import schedule
import threading

NYSE_LINK = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
NASDAQ_LINK = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"
 
SCRAPER = StockScraper()

SCRAPER.fillTickerData(LOC = NYSE_LINK)
SCRAPER.fillTickerData(LOC = NASDAQ_LINK, exchangeTitle = "Listing Exchange", exchangeLetter='Q')
SCRAPER.outputToCSV(CSV_NAME = "../AGGREGATED_STOCK_DATA")
