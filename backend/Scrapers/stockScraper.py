import yfinance as yf
import pandas as pd
from newsScraper import NewsScraper
import time
import sys

# NYSE: "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
# NASDAQ: "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"


class StockScraper:

    def __init__(self):
        self.COLUMNS = ['Symbol', 'shortName', 'forwardPE', 'currentRatio', 'shortRatio', 
                        'marketCap', 'sector', 'industry', 'sentiment', 'confidence']

        self.tickerData = []
        self.NEWS_SCRAPER = NewsScraper()


    def progressBar(self, count, total, width=50):
        percent = (count / total) * 100
        filledLength = int(width * count // total)

        bar = '[' + '#' * filledLength + '-' * (width - filledLength) + ']'
        sys.stdout.write(f'\r{bar} {percent:.1f}%')
        sys.stdout.flush()

    
    def processStock(self, ticker):
        info = yf.Ticker(ticker)

        try:
            if not info or not info.info: raise KeyError()
            currData = [ticker]
            for col in range(1, len(self.COLUMNS) - 2):
                currData.append(info.info[self.COLUMNS[col]])

            sentiment = self.NEWS_SCRAPER.sentimentAnalysis(ticker)
            currData.append(sentiment['label'])
            currData.append(sentiment['confidence'])

            return currData

        except (KeyError, AttributeError):
            return 'INVALID_STOCK'
        except Exception as e:
            errorStr = f'{e}'
            return 'RATE_LIMITED' if 'rate' in errorStr.lower() else 'INVALID_STOCK'


    def fillTickerData(self, exchangeTitle = "Exchange", exchangeLetter = 'N', symbolTitle = 'NASDAQ Symbol',
                       LOC = "", SEPARATOR = '|'):

        startTime = time.time()

        errorFile = open("error_log.txt", "a")
        DF = None
        try:
            DF = pd.read_csv(LOC, sep=SEPARATOR)
        except:
            errorFile.write(f"Could not read {LOC}\n")
            return -1

        DF = DF[(DF[exchangeTitle] == exchangeLetter) & (DF['ETF'] != 'Y') & 
                          (DF[symbolTitle].str.isalpha())]

        SYMBOLS = DF[symbolTitle].tolist()
        LIMIT = len(SYMBOLS)
        
        errorFile.write(f"Beginning processing for {LOC}\n")
        print("Beginning processing...")

        index = 0
        while index < LIMIT:
            ticker = SYMBOLS[index]

            try:
                currData = self.processStock(ticker)

                if currData == 'RATE_LIMITED':
                    errorFile.write(f'Rate limited on {ticker}\n')
                    index -= 1
                    time.sleep(30)

                elif currData != 'INVALID_STOCK':
                    self.tickerData.append(currData)

                self.progressBar(index, LIMIT)
                time.sleep(0.75)
                index += 1

            except KeyboardInterrupt:
                break

        errorFile.close()

        endTime = time.time()
        return endTime - startTime

    
    def outputToCSV(self, CSV_NAME):
        OBJECTIVE_DATA_DF = pd.DataFrame(self.tickerData, columns=self.COLUMNS)
        OBJECTIVE_DATA_DF.to_csv(CSV_NAME + '.csv', index = False)


