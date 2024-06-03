import json
import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

class QueryHandler:
    def __init__(self, model_dir, log_file):
        self.model_dir = model_dir
        self.log_file = log_file
        self.vectorizer, self.tfidf_matrix, self.queries = self.load_model_and_matrix()
        self.log_data = self.load_log_data()

    def read_queries_from_files(self, file_paths, encoding='utf-8'):
        queries = []
        for file_path in file_paths:
            with open(file_path, 'r', encoding=encoding) as file:
                for line in file:
                    query_object = json.loads(line)
                    queries.append(query_object['text'])
        return queries

    def train_tfidf_model(self, queries):
        vectorizer = TfidfVectorizer().fit(queries)
        tfidf_matrix = vectorizer.transform(queries)
        return vectorizer, tfidf_matrix

    def save_model_and_matrix(self, vectorizer, tfidf_matrix, queries):
        joblib.dump(vectorizer, os.path.join(self.model_dir, 'tfidf_vectorizer.pkl'))
        joblib.dump(tfidf_matrix, os.path.join(self.model_dir, 'tfidf_matrix.pkl'))
        joblib.dump(queries, os.path.join(self.model_dir, 'queries_list.pkl'))
        print("تم حفظ النموذج بنجاح")

    def load_model_and_matrix(self):
        vectorizer = joblib.load(os.path.join(self.model_dir, 'tfidf_vectorizer.pkl'))
        tfidf_matrix = joblib.load(os.path.join(self.model_dir, 'tfidf_matrix.pkl'))
        queries = joblib.load(os.path.join(self.model_dir, 'queries_list.pkl'))
        return vectorizer, tfidf_matrix, queries

    def correct_spelling_and_grammar(self, text):
        blob = TextBlob(text)
        corrected_text = str(blob.correct())
        return corrected_text

    def get_suggestions_tfidf(self, prefix, n=5):
        prefix_tfidf = self.vectorizer.transform([prefix])
        similarities = cosine_similarity(prefix_tfidf, self.tfidf_matrix).flatten()
        indices = np.argsort(similarities, axis=0)[::-1][:n]
        
        suggestions = [self.queries[i] for i in indices if similarities[i] > 0]
        suggestions = sorted(suggestions, key=lambda x: self.log_data.get(x, 0), reverse=True)[:n]
        return suggestions

    def load_log_data(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                return json.load(file)
        return {}

    def save_log_data(self):
        with open(self.log_file, 'w') as file:
            json.dump(self.log_data, file)

    def update_log(self, text):
        self.log_data[text] = self.log_data.get(text, 0) + 1
        self.save_log_data()
