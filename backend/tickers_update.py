# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 23:02:20 2025

@author: pyagu
"""

import time
import pandas as pd
import yfinance as yf
fileDir = '.\\data.csv'
df = pd.read_csv(fileDir)
COLUMNS = ['ticker', 'shortName', 'dict_info', 'has_forwardPE', 'forwardPE',
           'currentRatio', 'shortRatio', 'marketCap', 'sector', 'industry']
infos = {}
count = 0
symbols = df['ticker']
def continuer(symbols, count, df):
    try:
        for i in range (count, len(df)) :
            print(symbols[i])
            count += 1
            try:
                time.sleep(0.5)
                infos[symbols[i]] = yf.Ticker(symbols[i]).info
            except:
                print(count)
                time.sleep(0.5)
                print('forwardPE' in yf.Ticker(symbols[i]).info)
    except:
        print('Skaramoosh')
        return continuer(symbols, count, df)
continuer(symbols, count, df)
for i in range(len(infos)):
    for j in COLUMNS:
        if (j == 'has_forwardPE') :
            df[j][i] = 'forwardPE' in infos[i]
        elif (df['has_forwardPE'][i] != True):
            df['forwardPE'][i] = 0
        else:
            df[j][i] = infos[i][j]

df.to_csv(fileDir)
