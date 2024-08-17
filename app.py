from models.sentiment_analysis_openai import SentimentAnalysisManager
from scrapping.tweets_scaping import TweetsScraperManager
from utils.clean_data import text_process_pipeline
from dotenv import load_dotenv
from apis.api_manager import get_cities_scrap
import pandas as pd
import logging
from utils.helpers import convert_df2json
load_dotenv(override=True)

# Logging configuration
logging.basicConfig(filename='error_logs.log', level=logging.ERROR) 

scrap_manager = TweetsScraperManager()
sentiment_manager = SentimentAnalysisManager()

for city_id, city_coordinates in get_cities_scrap():
    print(city_id, city_coordinates)
    data = scrap_manager.scrap_city(city_coordinates=city_coordinates, max_items=50)
    data = pd.DataFrame(data)
    data['text'] = data['text'].apply(text_process_pipeline)
    data = data.dropna(axis=0)
    sentiment_df = sentiment_manager.perfrom_data_sentiment(data,city_id)
    full_data = pd.merge(data, sentiment_df, on='id')
    full_data['city_id'] = city_id
    full_data.to_csv("full_data.csv")
    list_json = convert_df2json(full_data)
    print(list_json)
    