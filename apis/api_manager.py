import requests
import logging

cites_api_url = "https://brief-brightly-owl.ngrok-free.app/api/Destinations/cities-to-scrape"
send_tweets_sentiment_api = "https://brief-brightly-owl.ngrok-free.app/api/mediasources"
RADIUS = 30

def get_cities_scrap():
    response = requests.get(cites_api_url)
    if response.status_code == 200:
        data = response.json()
    else:
        logging.error(f"During Fetching Cities, API request failed with status code {response.status_code}")
    
    for item in data:
        coordinates = f"{item['coordinates']['lat']},{item['coordinates']['long']},{RADIUS}km"
        yield item['id'], coordinates

def send_tweets_sentiment(json_list):
    try:
        response = requests.post(send_tweets_sentiment_api, json=json_list)
        if response.status_code == 200:
            return True
        else:
            logging.error(f"Send Data: API request failed with status code {response.status_code}")
            return False
    except:
        logging.error("While Sending data to APi (DB)")
        return False



