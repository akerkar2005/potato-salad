import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch
import sys

class NewsScraper:

    def __init__(self):
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }

        # Load FinBERT model for sentiment analysis
        finbert_model = "ProsusAI/finbert"
        tokenizer = AutoTokenizer.from_pretrained(finbert_model)
        model = AutoModelForSequenceClassification.from_pretrained(finbert_model)

        # Access the GPU if available
        device = torch.device("cpu")
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")

        self.sentimentPipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if device.type == "mps" else -1)
        self.SENTIMENT_LIMIT = 400


    def sentimentAnalysis(self, ticker):
        stockNewsDict = self.getNews(ticker)
        stockNews = [f"{title} : {desc}." for title,desc in stockNewsDict.items()]
        stockNews = ' '.join(stockNews)
        if len(stockNews) > self.SENTIMENT_LIMIT * 4: stockNews = stockNews[:self.SENTIMENT_LIMIT * 4]

        # Perform sentiment analysis
        sentiment_result = self.sentimentPipeline(stockNews)[0]
        sentiment_label = sentiment_result["label"]
        sentiment_score = sentiment_result["score"]

        return {'label': sentiment_label, 'confidence': sentiment_score}



    def getNews(self, stockTicker, printOut=False):

        response = requests.get('https://finance.yahoo.com/quote/' + stockTicker + '/news', headers=self.HEADERS)
        parser = BeautifulSoup(response.text, 'html.parser')

        articles = parser.select('a .yf-82qtw3')

        articlesDict = {}
        lastName = None
        for article in articles:
            if article.name == 'h3': lastName = article.text
            else: articlesDict[lastName] = article.text

        if printOut:
            for key in articlesDict:
                print("ARTICLE TITLE: " + key)
                print("DESCRIPTION: " + articlesDict[key])
                print("------------------------------------------------------------------------")
    
        return articlesDict

