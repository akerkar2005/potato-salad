import pandas as pd
BILLION = 10 ** 9

class StockSorter:

    def __init__(self, CSV_LOCATION = 'AGGREGATED_STOCK_DATA.csv'):
        STOCK_DATA_DF = pd.read_csv(CSV_LOCATION)
        STOCK_DATA_DF = STOCK_DATA_DF.fillna(0)
        self.COLUMNS = STOCK_DATA_DF.columns.tolist()
        STOCK_LIST = STOCK_DATA_DF.values.tolist()

        self.STOCK_DATA = []
        for row in STOCK_LIST:
            stockData = {self.COLUMNS[i]: row[i] for i in range(len(row))}
            self.STOCK_DATA.append(stockData)


    def customStockScore(self, stockData, preferences = {}):
        
        score = 0

        if 'maxMarketCap' in preferences:
            if stockData['marketCap'] <= preferences['maxMarketCap']:
                score += 10
        if 'minMarketCap' in preferences:
            if stockData['marketCap'] >= preferences['minMarketCap']:
                score += 10

        if 'sector' in preferences: score += 10 if stockData['sector'] in preferences['sector'] else 0
        if 'industry' in preferences: score += 15 if stockData['industry'] in preferences['industry'] else 0

        goodShortRatio = preferences['shortRatio'] if 'shortRatio' in preferences else 2.0
        badShortRatio = goodShortRatio * 2.0
        if stockData['shortRatio'] <= goodShortRatio:
            score += 2
        elif stockData['shortRatio'] >= badShortRatio:
            score -= (stockData['shortRatio'] - badShortRatio) / 2

        goodCurrentRatio = preferences['currentRatio'] if 'currentRatio' in preferences else 1.5
        score -= 2 * abs(stockData['currentRatio'] - goodCurrentRatio)

        goodPERatio = preferences['forwardPE'] if 'forwardPE' in preferences else 10
        badPERatio = goodPERatio * 2.0
        if stockData['forwardPE'] <= goodPERatio and stockData['forwardPE'] > 0: 
            score += 2
        elif stockData['forwardPE'] >= badPERatio:
            score -= (stockData['forwardPE'] - badPERatio) / 10
        elif stockData['forwardPE'] <= 0:
            score -= 5

        return score

    
    def getUniqueIndustries(self):
        industries = set()
        for item in self.STOCK_DATA:
            industries.add(item['industry'])

        return list(industries)
    
    def getUniqueSectors(self):
        sectors = set()
        for item in self.STOCK_DATA:
            sectors.add(item['sector'])

        return list(sectors)


    def sortWithPreferences(self, preferences={}):
        SORTED_DATA = sorted(self.STOCK_DATA, key=lambda stockData: self.customStockScore(stockData, preferences), reverse = True)
        return SORTED_DATA
