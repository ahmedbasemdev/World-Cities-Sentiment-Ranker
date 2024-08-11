from models.sentiment_analysis import SentimentAnalysisManager
from scapping.tweets_scaping import *
from dotenv import load_dotenv
from apis.api_manager import get_cities_scrap

load_dotenv()


for city in get_cities_scrap():
    print(city)