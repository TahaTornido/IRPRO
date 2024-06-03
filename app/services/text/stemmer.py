import nltk
from nltk.stem import PorterStemmer
nltk.download('punkt')
def stem_tokens(tokens):
    # إنشاء كائن PorterStemmer
    stemmer = PorterStemmer()
    
    # تطبيق التجزئة على كل توكن
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    
    return stemmed_tokens
