import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tkinter as tk
import joblib
import os
from textblob import TextBlob
# جزء القراءة والتدريب وحفظ النموذج
def read_queries_from_files(file_paths, encoding='utf-8'):
    queries = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding=encoding) as file:
            for line in file:
                query_object = json.loads(line)
                queries.append(query_object['text'])
    return queries

def train_tfidf_model(queries):
    vectorizer = TfidfVectorizer().fit(queries)
    tfidf_matrix = vectorizer.transform(queries)
    return vectorizer, tfidf_matrix

def save_model_and_matrix(vectorizer, tfidf_matrix, queries, save_dir):
    joblib.dump(vectorizer, os.path.join(save_dir, 'tfidf_vectorizer.pkl'))
    joblib.dump(tfidf_matrix, os.path.join(save_dir, 'tfidf_matrix.pkl'))
    joblib.dump(queries, os.path.join(save_dir, 'queries_list.pkl'))
    print("تم حفظ النموذج بنجاح")

# جزء تحميل النموذج والمصفوفة
def load_model_and_matrix(model_dir):
    vectorizer = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
    tfidf_matrix = joblib.load(os.path.join(model_dir, 'tfidf_matrix.pkl'))
    queries = joblib.load(os.path.join(model_dir, 'queries_list.pkl'))
    return vectorizer, tfidf_matrix, queries
