import pandas as pd

class StockSorter:

    def __init__(self, CSV_LOCATION = 'SENTIMENT_STOCK_DATA.csv'):
        STOCK_DATA_DF = pd.read_csv(CSV_LOCATION)
        STOCK_DATA_DF = STOCK_DATA_DF.fillna(0)
        STOCK_DATA_DF = STOCK_DATA_DF.loc[:, ~STOCK_DATA_DF.columns.str.contains('^Unnamed')]
        self.COLUMNS = STOCK_DATA_DF.columns.tolist()
        STOCK_LIST = STOCK_DATA_DF.values.tolist()
        self.SENTIMENT_TO_SCORE = {'positive': 1, 'neutral': 0, 'negative': -1}

        self.STOCK_DATA = []
        for row in STOCK_LIST:
            stockData = {self.COLUMNS[i]: row[i] for i in range(len(row))}
            self.STOCK_DATA.append(stockData)


    def customStockScore(self, stockData, preferences = {}):
        
        score = 5 * self.SENTIMENT_TO_SCORE[stockData['sentiment']] * stockData['confidence']

        if 'maxMarketCap' in preferences:
            if stockData['marketCap'] <= float(preferences['maxMarketCap']):
                score += 4
        if 'minMarketCap' in preferences:
            if stockData['marketCap'] >= float(preferences['minMarketCap']):
                score += 4

        if 'sector' in preferences: score += 10 if stockData['sector'] in preferences['sector'] else 0
        if 'industry' in preferences: score += 10 if stockData['industry'] in preferences['industry'] else 0

        goodShortRatio = float(preferences['shortRatio']) if 'shortRatio' in preferences else 2.0
        badShortRatio = goodShortRatio * 2.0
        if stockData['shortRatio'] <= goodShortRatio:
            score += (max((goodShortRatio - stockData['shortRatio']) / 2, 2))
        elif stockData['shortRatio'] >= badShortRatio:
            score -= (stockData['shortRatio'] - badShortRatio) / 2

        goodCurrentRatio = float(preferences['currentRatio']) if 'currentRatio' in preferences else 1.5
        score -= 2 * abs(stockData['currentRatio'] - goodCurrentRatio)

        goodPERatio = float(preferences['forwardPE']) if 'forwardPE' in preferences else 25
        badPERatio = goodPERatio * 2.0
        if stockData['forwardPE'] <= goodPERatio and stockData['forwardPE'] > 0: 
            score += 2
        elif stockData['forwardPE'] >= badPERatio:
            score -= (stockData['forwardPE'] - badPERatio) / 3
        elif stockData['forwardPE'] <= 0:
            score -= 15

        return score

    
    def getUniqueIndustries(self):
        industries = set()
        for item in self.STOCK_DATA:
            industries.add(str(item['industry']))

        if '0' in industries: industries.remove('0')

        return list(industries)
    
    def getUniqueSectors(self):
        sectors = set()
        for item in self.STOCK_DATA:
            sectors.add(str(item['sector']))

        if '0' in sectors: sectors.remove('0')
    
        return list(sectors)


    def sortWithPreferences(self, preferences={}):
        SORTED_DATA = sorted(self.STOCK_DATA, key=lambda stockData: self.customStockScore(stockData, preferences), reverse = True)
        return SORTED_DATA


obj = StockSorter()
