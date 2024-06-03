from app.services.text.date_bracket import process_and_standardize_dates_brackets
from app.services.text.equations import remove_equations
from app.services.text.lemmatize import lemmatize_tokens
from app.services.text.lowercase import convert_to_lowercase
from app.services.text.phonetic import remove_phonetic_notation
from app.services.text.puncutation import remove_punctuation
from app.services.text.sanitize import sanitize_query
from app.services.text.stemmer import stem_tokens
from app.services.text.stopwords import remove_stopwords
from services.text.tokenize import tokenize_text
from app.services.text.tokenize import join_tokens
from app.services.text.urls import remove_urls

def process_text(text):
    text_without_phonetic=remove_phonetic_notation(text)
    text_without_equations=remove_equations(text_without_phonetic)
    text_sent=sanitize_query(text_without_equations)
    tokens = tokenize_text(text_sent)
    tokens=convert_to_lowercase(tokens)
    tokens=remove_urls(tokens)
    tokens=remove_punctuation(tokens)
    tokens=process_and_standardize_dates_brackets(tokens)
    tokens = remove_stopwords(tokens)
    tokens=stem_tokens(tokens)
    tokens=lemmatize_tokens(tokens)
    tokens =join_tokens(tokens)
    return tokens