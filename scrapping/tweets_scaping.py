import requests
import os

class TweetsScraperManager:
    def __init__(self):
        self.token = os.environ['APIFY_TOKEN']
        self.actor_id = "61RPP7dywgiy0JPD0"
        self.actor_api = f"https://api.apify.com/v2/acts/{self.actor_id}/run-sync"

    def scrap_city(self, city_coordinates, max_items:int=50):
        self.__run_scrapping_actor(city_coordinates, max_items)
        self.data_id = self.__get_data_id()
        if self.data_id == False:
            print("None")
            return None
        data = self.__retrive_data()
        return data

    def __run_scrapping_actor(self, city_coordinates, max_items:int=50):
        # Define the input parameters for the API
        inputs = {
            "geocode": city_coordinates,
            "minimumFavorites": 100,
            "minimumRetweets":100,
            "query": "news",
            "onlyVerifiedUsers":True,
            "searchMode": "recent",
        }

        params = {"token": self.token, "maxItems": max_items}

        try:
            response = requests.post(self.actor_api, json=inputs, params=params) 
            data = response.json()
            print(data)
        except:
            pass

        return True
    
    def __get_data_id(self):
        url = f"https://api.apify.com/v2/actor-runs?token={self.token}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            data_id = data['data']['items'][-1]['defaultDatasetId']
            print(data_id)
            return data_id
            
        else:
            return False
        
    def __retrive_data(self):
        url = f"https://api.apify.com/v2/datasets/{self.data_id}/items?format=json"
        headers = {
            "Authorization": f"Bearer {os.environ['APIFY_TOKEN']}"
        }
        response = requests.get(url, headers=headers, params={"clean":"true","view":"overview"})
        if response.status_code == 200:
            data = response.json()
            return data  
        else:
            return False
    

