from models.sentiment_analysis import SentimentAnalysisManager
from scrapping.tweets_scaping import TweetsScraperManager
from utils.clean_data import text_process_pipeline
from dotenv import load_dotenv
from apis.api_manager import get_cities_scrap
import pandas as pd
load_dotenv()

scrap_manager = TweetsScraperManager()


for city in get_cities_scrap():
    data = scrap_manager.scrap_city(city=city, max_items=4)
    data = pd.DataFrame(data)
    data['text'] = data['text'].apply(text_process_pipeline)
    data = data.dropna(axis=0)

    ############################################
    ## Sending data to API to be stored in DB ##
    ############################################