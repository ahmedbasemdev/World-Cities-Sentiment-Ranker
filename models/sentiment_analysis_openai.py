import requests
import json
from openai import OpenAI
import os
import time 
import pandas as pd
import logging

system_prompt = "You are an AI language model trained to analyze and detect the sentiment of tweet."

class SentimentAnalysisManager:
    def __init__(self, model_name:str="gpt-4-turbo") -> None:
        self.model_name = model_name
        self.client = OpenAI()
        self.batch_file_name = "batch_tasks.jsonl"

    def __generate_tasks(self, data):
        tasks = []
        for idx in range(len(data)):
            row = data.iloc[idx]
            tweet_id = row.id
            text = row.text
            task = {
                "custom_id": f"{tweet_id}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4-turbo",
                    "temperature": 0,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": f"Analyze the following tweet and determine if the sentiment is: positive, negative or neutral. Return only a single word, either POSITIVE, NEGATIVE or NEUTRAL: {text}"
                        }
                    ],
                }
            }

            tasks.append(task)
        return tasks
    
    def __generate_jsonl_file(self, tasks):
        print("task",len(tasks))
        with open(self.batch_file_name, 'w') as file:
            for task in tasks:
                file.write(json.dumps(task) + "\n")
        return True
    
    def __run_batch(self):
        batch_file = self.client.files.create(
        file=open(self.batch_file_name, "rb"),
        purpose="batch")

        try:
            batch_job = self.client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h")
            return batch_job.id
        except:
            logging.error("While Creating Batch `GPT Side`, check billing")
            return False

        
    
    def __convert_results_df(self, results):
        results = results.split("\n")
        print(len(results))
        data_results = {"id":[], "sentiment":[]}
        for result in results:
            if len(result) < 10:
                continue
            try:
                json_result = json.loads(result)
            except:
                logging.error(f"During Converting Data to Json {result}")
                continue

            tweet_id = json_result['custom_id']
            sentiment = json_result['response']['body']['choices'][0]['message']['content'].lower()
            data_results['id'].append(tweet_id)
            data_results['sentiment'].append(sentiment)
        df = pd.DataFrame(data_results)

        return df

    
    def perfrom_data_sentiment(self, data, city:str):
        tasks = self.__generate_tasks(data)
        self.__generate_jsonl_file(tasks)
        batch_id = self.__run_batch()
        if batch_id == False:
            return None
        batch_job = self.client.batches.retrieve(batch_id)
        while batch_job.status not in ["completed","failed","expired"]:
            batch_job = self.client.batches.retrieve(batch_job.id)
            print(batch_job.status)
            time.sleep(60)
        else:
            successed_precentage = (batch_job.request_counts.completed + batch_job.request_counts.failed) / batch_job.request_counts.total
        
        if successed_precentage > .8 :
            result_file_id = batch_job.output_file_id
            results = self.client.files.content(result_file_id).text
        else:
            logging.error(f"Number of Success Tasks Less than 80% for city = {city}")
        
        df = self.__convert_results_df(results)

        return df



