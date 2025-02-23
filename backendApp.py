from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stockSorter import StockSorter
from newsScraper import NewsScraper
import uvicorn

app = FastAPI()

# Allow the front end to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Front end is running on port 5173
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],
)

STOCK_SORTER = StockSorter()
NEWS_SCRAPER = NewsScraper()

@app.post('/api/launch')
async def launchApp():
    # list of dictionaries with stuff like marketCap, shortRatio, forwardPE, ticker, shortName, etc
    defaultList = STOCK_SORTER.sortWithPreferences()
    stockList = []
    for row in defaultList:
        newRow = {}
        newRow['ticker'] = row['ticker']
        newRow['shortName'] = row['shortName']
        newRow['currentRatio'] = row['currentRatio']
        newRow['shortRatio'] = row['shortRatio']
        newRow['marketCap'] = row['marketCap']
        newRow['industry'] = row['industry']
        newRow['sector'] = row['sector']
        newRow['sentiment'] = row['sentiment']
        newRow['confidence'] = row['confidence']

        stockList.append(newRow)

    # list of strings
    uniqueSectors = STOCK_SORTER.getUniqueSectors()

    # list of strings
    uniqueIndustries = STOCK_SORTER.getUniqueIndustries()

    return {
        'sortedStocks': stockList,
        'sectors': uniqueSectors,
        'industries': uniqueIndustries
    }
    

@app.post("/api/update")
async def updateSortedList(preferences: dict):
    """
    Analyze the sentiment of a given stock ticker
    """
    
    newList = STOCK_SORTER.sortWithPreferences(preferences)
    sortedList = []
    for row in newList:
        newRow = {}
        newRow['ticker'] = row['ticker']
        newRow['shortName'] = row['shortName']
        newRow['currentRatio'] = row['currentRatio']
        newRow['shortRatio'] = row['shortRatio']
        newRow['marketCap'] = row['marketCap']
        newRow['industry'] = row['industry']
        newRow['sector'] = row['sector']
        newRow['sentiment'] = row['sentiment']
        newRow['confidence'] = row['confidence']

        sortedList.append(newRow)

    return {
        "sortedStocks": sortedList
    }

uvicorn.run(app, host="127.0.0.1", port=3000)
