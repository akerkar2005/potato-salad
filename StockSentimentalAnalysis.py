from fastapi import FastAPI, Query
import requests
import trafilatura
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch
import modal
import os

app = FastAPI()

# Load FinBERT model for sentiment analysis
finbert_model = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(finbert_model)
model = AutoModelForSequenceClassification.from_pretrained(finbert_model)
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if device.type == "mps" else -1)

# Initialize Modal and retrieve the OpenAI API key
app_modal = modal.App()
secrets = modal.Secret.from_name("openai-api-key")

# Explicitly add local Python source to the Modal image
image_with_source = modal.Image.debian_slim().add_local_python_source("_remote_module_non_scriptable")

@app_modal.function(image=image_with_source)
def get_openai_client():
    import openai
    openai.api_key = secrets["OPENAI_API_KEY"]
    return openai

@app.post("/analyze")
def analyze_stock(ticker: str = Query(..., description="Stock ticker symbol")):
    """
    Analyze the sentiment of a given stock ticker and provide investment reasoning.
    """
    # Placeholder for news/article retrieval (to be implemented later)
    news_article = f"Latest news about {ticker}. Apple's earnings report exceeded expectations."
    
    # Perform sentiment analysis
    sentiment_result = sentiment_pipeline(news_article)[0]
    sentiment_label = sentiment_result["label"]
    sentiment_score = sentiment_result["score"]

    # Generate investment reasoning using OpenAI
    reasoning_prompt = (
        f"The sentiment for stock {ticker} is {sentiment_label}, and we can say this with a confidence level of {sentiment_score}. The P/E ratio is 40. Here is a news article excerpt that goes over what the stock sentiment is exactly: [example]. Given this excerpt and the sentiment, can you indicate how this will impact investment decisions? How would one intelligently go through with investing given you have a budget of 1,000 dollars? Please make this a structured API response."
    )
    
    # Use Modal to get the OpenAI client
    openai_client = get_openai_client.call()
    response = openai_client.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": reasoning_prompt}]
    )
    investment_reasoning = response.choices[0].message.content    
    
    return {
        "ticker": ticker,
        "sentiment": sentiment_label,
        "reasoning": investment_reasoning
    }