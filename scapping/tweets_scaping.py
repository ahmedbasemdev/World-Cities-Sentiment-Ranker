import requests
import os

class TweetsScraperManager:
    def __init__(self):
        self.token = os.environ['APIFY_TOKEN']

    def 