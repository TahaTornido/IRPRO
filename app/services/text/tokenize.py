import nltk
from nltk.tokenize import word_tokenize

def tokenize_text(text):
    """
    This function takes a text string as input and returns a list of words (tokens) using NLTK's word_tokenize function.
    
    Args:
    text (str): The input text to be tokenized.
    
    Returns:
    list: A list of words (tokens).
    """
    tokens = word_tokenize(text)
    return tokens
def join_tokens(tokens):
    """
    يأخذ سلسلة من الtokens ويقوم بعملية join لها لإعادة نص موحد.
    
    Args:
    tokens (list of str): قائمة من الكلمات (tokens).
    
    Returns:
    str: نص موحد.
    """
    return ' '.join(tokens)
