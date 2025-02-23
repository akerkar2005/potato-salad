import yfinance as yf
import pandas as pd
import time
import sys

COLUMNS = ['Symbol', 'shortName', 'forwardPE', 'currentRatio', 'shortRatio', 'marketCap', 'sector', 'industry']
BILLION = 10 ** 9


def progressBar(count, total, width=50):
    percent = (count / total) * 100
    filledLength = int(width * count // total)

    bar = '[' + '#' * filledLength + '-' * (width - filledLength) + ']'
    sys.stdout.write(f'\r{bar} {percent:.1f}%')
    sys.stdout.flush()

    
def processStock(ticker):
    info = yf.Ticker(ticker)
    try:

        if not info or not info.info: raise KeyError()
        currData = [ticker]
        for col in range(1, len(COLUMNS)):
            currData.append(info.info[COLUMNS[col]])

        return currData

    except (KeyError, AttributeError):
        return 'INVALID_STOCK'
    except Exception as e:
        errorStr = f'{e}'
        return 'RATE_LIMITED' if 'rate' in errorStr.lower() else 'INVALID_STOCK'


startTime = time.time()

NYSE_DF = pd.read_csv("https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt", sep = '|') 
NYSE_DF = NYSE_DF[(NYSE_DF['Exchange'] == 'N') & (NYSE_DF['ETF'] != 'Y') & (NYSE_DF['NASDAQ Symbol'].str.isalpha())]

NYSE_SYMBOLS = NYSE_DF['NASDAQ Symbol'].tolist()

tickerData = []
LIMIT = len(NYSE_SYMBOLS)

print("Beginning NYSE processing...")

index = 0
while index < LIMIT:
    ticker = NYSE_SYMBOLS[index]

    try:
        currData = processStock(ticker)

        if currData == 'RATE_LIMITED':
            print(f'Rate limited on {ticker}')
            index -= 1
            time.sleep(30)

        elif currData != 'INVALID_STOCK':
            tickerData.append(currData)

        progressBar(index, len(NYSE_SYMBOLS))
        time.sleep(0.75)
        index += 1

    except KeyboardInterrupt:
        break


NYSE_OBJECTIVE_DATA_DF = pd.DataFrame(tickerData, columns=COLUMNS)
NYSE_OBJECTIVE_DATA_DF.to_csv('NYSE_DATA.csv', index = False)

totalTime = time.time() - startTime
print(f"\nTime Taken: {totalTime:.4f} seconds to process {len(NYSE_SYMBOLS)} symbols")
