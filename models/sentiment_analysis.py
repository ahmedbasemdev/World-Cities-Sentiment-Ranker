import ollama

class SentimentAnalysisManager:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    def perform_sentiment(self, text):

        messages = [
            {"role": "system", 
             "content": "You are an AI language model trained to analyze and detect the sentiment of tweet."},
            {"role": "user", "content": f"""
            Analyze the following tweet and determine if the sentiment is: positive, negative or neutral. Return only a single word, either POSITIVE, NEGATIVE or NEUTRAL: {text}
            """}]
        result = ollama.chat(model=self.model_name, messages=messages)
        content = result['message']['content'].split(":\n")[-1]
        print(content)
        return content.strip()

