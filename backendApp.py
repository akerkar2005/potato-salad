from fastapi import FastAPI
from stockSorter import StockSorter
from newsScraper import NewsScraper
import uvicorn

app = FastAPI()


STOCK_SORTER = StockSorter()
NEWS_SCRAPER = NewsScraper()

@app.post('/api/launch')
async def launchApp():
    # list of dictionaries with stuff like marketCap, shortRatio, forwardPE, ticker, shortName, etc
    defaultList = STOCK_SORTER.sortWithPreferences()

    # list of strings
    uniqueSectors = STOCK_SORTER.getUniqueSectors()

    # list of strings
    uniqueIndustries = STOCK_SORTER.getUniqueIndustries()

    return {
        'sortedStocks': defaultList,
        'sectors': uniqueSectors,
        'industries': uniqueIndustries
    }
    

@app.post("/api/update")
async def updateSortedList(preferences: dict):
    """
    Analyze the sentiment of a given stock ticker
    """
    
    sortedList = STOCK_SORTER.sortWithPreferences(preferences)

    return {
        "sortedStocks": sortedList
    }

uvicorn.run(app, host="127.0.0.1", port=3000)
