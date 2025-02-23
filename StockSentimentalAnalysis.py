from fastapi import FastAPI, Query
import yfinance as yf
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import openai
import os

app = FastAPI()

# Load FinBERT model for sentiment analysis
finbert_model = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(finbert_model)
model = AutoModelForSequenceClassification.from_pretrained(finbert_model)
OPENAI_API_KEY="ak-BDlN7PbYDtgeHy8fJl65Wr "

# Assign device correctly
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cuda" if torch.cuda.is_available() else "cpu")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if device.type == "cuda" else -1)

# Set up OpenAI API key
#openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable

@app.post("/analyze")
def analyze_stock(ticker: str = Query(..., description="Stock ticker symbol")):
    """
    Analyze the sentiment of a given stock ticker and provide investment reasoning.
    """
    # Get stock P/E ratio
    #stock = yf.Ticker(ticker)
    pe_ratio = 40 
    #pe_ratio = stock.info.get("trailingPE", "N/A")  # Get real P/E ratio

    # Placeholder for news retrieval (to be implemented later)
    news_article = f"Latest news about {ticker}. Apple's earnings report exceeded expectations."

    # Perform sentiment analysis
    sentiment_result = sentiment_pipeline(news_article)[0]
    sentiment_label = sentiment_result["label"]
    sentiment_score = sentiment_result["score"]

    # Generate investment reasoning using OpenAI
    reasoning_prompt = (
        f"The sentiment for stock {ticker} is {sentiment_label}, and we can say this with a confidence level of {sentiment_score}. "
        f"The P/E ratio is {pe_ratio}. Here is a news article excerpt that goes over what the stock sentiment is exactly: [example]. "
        "Given this excerpt and the sentiment, can you indicate how this will impact investment decisions? "
        "How would one intelligently go through with investing given you have a budget of 1,000 dollars? "
        "Please make this a structured API response."
    )
    

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": reasoning_prompt}]
    )
