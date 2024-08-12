import re

def remove_link_hashtag_mentions(text):
    # Remove URLs (links)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove Twitter mentions (e.g., @username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags (e.g., #hashtag)
    text = re.sub(r'#\w+', '', text)
    
    # Remove any remaining special characters and extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text




def text_process_pipeline(text):
    text = remove_link_hashtag_mentions(text)
    text = text.strip()
    if len(text.split()) < 10:
        return None

    return text