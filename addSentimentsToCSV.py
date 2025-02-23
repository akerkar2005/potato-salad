import pandas as pd
from newsScraper import NewsScraper
import sys

def progressBar(count, total, width=50):
    percent = (count / total) * 100
    filledLength = int(width * count // total)

    bar = '[' + '#' * filledLength + '-' * (width - filledLength) + ']'
    sys.stdout.write(f'\r{bar} {percent:.1f}%')
    sys.stdout.flush()


NEWS_SCRAPER = NewsScraper()

class Temp:
    def __init__(self, STOCK_DF):
        self.COUNT = 0
        self.LENGTH = len(STOCK_DF)

    def getTupleSentiment(self, ticker):
        sentiment = NEWS_SCRAPER.sentimentAnalysis(ticker)
        self.COUNT += 1
        progressBar(self.COUNT, self.LENGTH, width=100)
        return (sentiment['label'], sentiment['confidence'])

STOCK_DF = pd.read_csv('AGGREGATED_STOCK_DATA.csv')
temp = Temp(STOCK_DF)

STOCK_DF[['sentiment', 'confidence']] = STOCK_DF['ticker'].apply(lambda x: pd.Series(temp.getTupleSentiment(x)))

STOCK_DF.to_csv('SENTIMENT_STOCK_DATA.csv', index = False)


