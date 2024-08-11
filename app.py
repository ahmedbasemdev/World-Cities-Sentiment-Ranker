from models.sentiment_analysis import SentimentAnalysisManager
from scapping.tweets_scaping import TweetsScraperManager
from scapping.tweets_scaping import *
from dotenv import load_dotenv
from apis.api_manager import get_cities_scrap

load_dotenv()

scrap_manager = TweetsScraperManager()
for city in get_cities_scrap():
    data = scrap_manager.scrap_city(city=city, max_items=4)
    for sample in data:
        print(sample['text'])
        print("-" * 30)