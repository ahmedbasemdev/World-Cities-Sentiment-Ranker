import requests
import logging
cites_api_url = "https://brief-brightly-owl.ngrok-free.app/api/Destinations/cities-to-scrape"
def get_cities_scrap():
    response = requests.get(cites_api_url)
    if response.status_code == 200:
        data = response.json()
    else:
        logging.error(f"During Fetching Cities, API request failed with status code {response.status_code}")
    
    for item in data:
        coordinates = f"{item['coordinates']['lat']},{item['coordinates']['long']},10km"
        yield item['id'], coordinates

