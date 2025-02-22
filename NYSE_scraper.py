import yfinance as yf
import pandas as pd
import time
import sys

def progressBar(count, total, width=50):
    percent = (count / total) * 100
    filledLength = int(width * count // total)

    bar = '[' + '#' * filledLength + '-' * (width - filledLength) + ']'
    sys.stdout.write(f'\r{bar} {percent:.1f}%')
    sys.stdout.flush()

startTime = time.time()

NYSE_DF = pd.read_csv("https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt", sep = '|') 
NYSE_DF = NYSE_DF[(NYSE_DF['Exchange'] == 'N') & (NYSE_DF['ETF'] != 'Y') & (NYSE_DF['NASDAQ Symbol'].str.isalpha())]

NYSE_SYMBOLS = NYSE_DF['NASDAQ Symbol'].tolist()
tickerData = []

print("Beginning NYSE processing...")

for i,ticker in enumerate(NYSE_SYMBOLS):
    info = yf.Ticker(ticker)

    try:
        if not info: raise KeyError()
        tickerData.append((ticker, info.info['forwardPE']))
        progressBar(i, len(NYSE_SYMBOLS))

        time.sleep(0.75)

    except KeyboardInterrupt:
        sys.exit(0)
    except KeyError:
        pass
    except:
        print(f"Rate limited on {ticker}")
        time.sleep(60)


with open('NYSE_DATA.txt', 'w') as nyseFile:
    for ticker, ratio in tickerData:
        nyseFile.write(ticker + ',')
        nyseFile.write(str(ratio) + '\n')

totalTime = time.time() - startTime
print(f"Time Taken: {totalTime:.4f} seconds to process {len(NYSE_SYMBOLS)} symbols")
