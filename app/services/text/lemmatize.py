import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from nltk.corpus import wordnet

nltk.download('words')
nltk.download('averaged_perceptron_tagger')
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        'J': wordnet.ADJ,
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }
    return tag_dict.get(tag, wordnet.NOUN)
def lemmatize_tokens(tokens):
    """
    This function takes a list of tokens and performs lemmatization on them.
    
    Args:
    tokens (list): The input list of tokens.
    
    Returns:
    list: A list of lemmatized tokens.
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    return lemmatized_tokens
