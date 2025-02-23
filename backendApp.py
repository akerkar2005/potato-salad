from fastapi import FastAPI
from stockSorter import StockSorter
from newsScraper import NewsScraper
import uvicorn

app = FastAPI()


STOCK_SORTER = StockSorter()
NEWS_SCRAPER = NewsScraper()

@app.get('/')
async def launchApp():
    defaultList = STOCK_SORTER.sortWithPreferences()
    uniqueSectors = STOCK_SORTER.getUniqueSectors()
    uniqueIndustries = STOCK_SORTER.getUniqueIndustries()

    print(uniqueSectors)
    print(uniqueIndustries)

    return {
        'sortedStocks': defaultList,
        'sectors': uniqueSectors,
        'industries': uniqueIndustries
    }
    

@app.get("/analyze/{ticker}")
async def analyze_stock(ticker: str):
    """
    Analyze the sentiment of a given stock ticker
    """
    print(ticker)
    sentiment = NEWS_SCRAPER.sentimentAnalysis(ticker)
    sentiment_label = sentiment['label']
    sentiment_score = sentiment['confidence']
    
    return {
        "ticker": ticker,
        "sentiment": sentiment_label,
        "score": sentiment_score
    }

uvicorn.run(app, host="127.0.0.1", port=8000)
