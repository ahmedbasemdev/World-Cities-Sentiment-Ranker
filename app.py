from models.sentiment_analysis_openai import SentimentAnalysisManager
from scrapping.tweets_scaping import TweetsScraperManager
from utils.clean_data import text_process_pipeline
from dotenv import load_dotenv
from apis.api_manager import get_cities_scrap
import pandas as pd
import logging

load_dotenv(override=True)

# Logging configuration
logging.basicConfig(filename='error_logs.log', level=logging.ERROR) 

scrap_manager = TweetsScraperManager()
sentimnet_manager = SentimentAnalysisManager()

for city in get_cities_scrap():
    data = scrap_manager.scrap_city(city=city, max_items=4)
    data = pd.DataFrame(data)
    data['text'] = data['text'].apply(text_process_pipeline)
    data = data.dropna(axis=0)
    sentiment_df = sentimnet_manager.perfrom_data_sentiment(data,city)
    full_data = pd.merge(data, sentiment_df, on='id')
    full_data.to_csv("full.csv")
    print(full_data)
    