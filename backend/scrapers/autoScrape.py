from stockScraper import StockScraper
import schedule
import threading

#NYSE_LINK = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
NASDAQ_LINK = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"

SCRAPER = StockScraper()

try:
    #SCRAPER.fillTickerData(LOC = NYSE_LINK)
    SCRAPER.fillTickerData(LOC = NASDAQ_LINK, exchangeTitle = "Listing Exchange", exchangeLetter='N')
    SCRAPER.outputToCSV(CSV_NAME = "../SENTIMENT_STOCK_DATA")
except KeyboardInterrupt:
    print("\nScraping interrupted by user. Saving partial data...")
    SCRAPER.outputToCSV(CSV_NAME = "../SENTIMENT_STOCK_DATA")