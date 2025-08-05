
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from stockSorter import StockSorter
import uvicorn
import humanize


app = FastAPI()

# Allow the front end to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://100.100.167.111:5173", "https://akerkar2005.github.io"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],
)

STOCK_SORTER = StockSorter()

@app.post('/api/launch')
async def launchApp():
    # list of dictionaries with stuff like marketCap, shortRatio, forwardPE, ticker, shortName, etc
    defaultList = STOCK_SORTER.sortWithPreferences({}, 50)
    stockList = []
    for row in defaultList:
        newRow = {}
        newRow['Ticker'] = row['ticker']
        newRow['Name'] = row['shortName']
        newRow['PE Ratio'] = round(row['forwardPE'], 2)
        newRow['Current Ratio'] = round(row['currentRatio'], 2)
        newRow['Short Ratio'] = round(row['shortRatio'], 2)
        newRow['Market Cap'] = humanize.intword(row['marketCap'])
        newRow['Sector'] = row['sector']
        newRow['Industry '] = row['industry']
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
    
    # Convert comma-separated strings to lists for compatibility
    prefs = preferences.copy()
    if 'industry' in prefs and isinstance(prefs['industry'], str):
        prefs['industry'] = [i for i in prefs['industry'].split(',') if i]
    if 'sector' in prefs and isinstance(prefs['sector'], str):
        prefs['sector'] = [s for s in prefs['sector'].split(',') if s]

    newList = STOCK_SORTER.sortWithPreferences(prefs, 50)
    sortedList = []
    for row in newList:
        newRow = {}
        newRow['Ticker'] = row['ticker']
        newRow['Name'] = row['shortName']
        newRow['PE Ratio'] = round(row['forwardPE'], 2)
        newRow['Current Ratio'] = round(row['currentRatio'], 2)
        newRow['Short Ratio'] = round(row['shortRatio'], 2)
        newRow['Market Cap'] = humanize.intword(row['marketCap'])
        newRow['Sector'] = row['sector']
        newRow['Industry '] = row['industry']
        newRow['sentiment'] = row['sentiment']
        newRow['confidence'] = row['confidence']

        sortedList.append(newRow)

    return {
        "sortedStocks": sortedList
    }


# Global OPTIONS handler for CORS preflight
@app.options("/{rest_of_path:path}")
async def options_handler(rest_of_path: str):
    return JSONResponse(content={})
