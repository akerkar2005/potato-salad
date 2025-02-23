import pandas as pd
preferences = {}

def customStockScore(stockData, preferences={}):
    stockData = {COLUMNS[i]: stockData[i] for i in range(len(stockData))}
    score = 0

    if 'maxMarketCap' in preferences:
        if stockData['marketCap'] <= preferences['maxMarketCap']:
            score += 4
    if 'minMarketCap' in preferences:
        if stockData['marketCap'] >= preferences['minMarketCap']:
            score += 4

    if 'sector' in preferences: score += 10 if stockData['sector'] in preferences['sector'] else 0
    if 'industry' in preferences: score += 10 if stockData['industry'] in preferences['industry'] else 0

    goodShortRatio = preferences['shortRatio'] if 'shortRatio' in preferences else 2.0
    badShortRatio = goodShortRatio * 2.0
    if stockData['shortRatio'] <= goodShortRatio:
        score += (max((goodShortRatio - stockData['shortRatio']) / 2, 2))
    elif stockData['shortRatio'] >= badShortRatio:
        score -= (stockData['shortRatio'] - badShortRatio) / 2

    goodCurrentRatio = preferences['currentRatio'] if 'currentRatio' in preferences else 1.5
    score -= 2 * abs(stockData['currentRatio'] - goodCurrentRatio)

    goodPERatio = preferences['forwardPE'] if 'forwardPE' in preferences else 25
    badPERatio = goodPERatio * 2.0
    if stockData['forwardPE'] <= goodPERatio and stockData['forwardPE'] > 0: 
        score += 2
    elif stockData['forwardPE'] >= badPERatio:
        score -= (stockData['forwardPE'] - badPERatio) / 3
    elif stockData['forwardPE'] <= 0:
        score -= 15

    return score


NYSE_STOCK_DATA_DF = pd.read_csv('NYSE_DATA.csv')
COLUMNS = NYSE_STOCK_DATA_DF.columns.tolist()

NYSE_STOCK_DATA = NYSE_STOCK_DATA_DF.values.tolist()
NYSE_STOCK_DATA.sort(key=lambda stockData: customStockScore(stockData, preferences), reverse = True)

print(COLUMNS)
for row in NYSE_STOCK_DATA[:5]:
    print(row)
