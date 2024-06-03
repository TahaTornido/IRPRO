import nltk
from nltk.corpus import stopwords
nltk.download('stopword')

def remove_stopwords(tokens):
    """
    This function takes a list of tokens and removes English stop words.
    
    Args:
    tokens (list): The input list of tokens.
    
    Returns:
    list: A list of tokens with stop words removed.
    """
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return filtered_tokens
