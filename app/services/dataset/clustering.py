import os
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pyterrier as pt
from sklearn.cluster import KMeans
from app.services.dataset.file_reader import json_files_iterator
from app.services.dataset.file_reader import document_iterator


def process_clustering(data_path, index_path, num_clusters, max_features=10000, overwrite=True):
    """
    Process documents from the specified data path, apply TF-IDF, cluster the documents, and create an index.

    Parameters:
    - data_path (str): The path to the directory containing JSON files.
    - index_path (str): The path where the index will be saved.
    - num_clusters (int): The number of clusters to create.
    - max_features (int): The maximum number of features for the TF-IDF vectorizer.
    - overwrite (bool): Whether to overwrite the existing index.

    Returns:
    - None
    """
    # خطوة 2: جمع الوثائق في قائمة لتحويلها إلى DataFrame
    documents = list(json_files_iterator(data_path))
    df = pd.DataFrame(documents)

    # خطوة 3: تطبيق TF-IDF على النصوص
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(df['text'])
    
    # خطوة 4: تجميع الوثائق باستخدام KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(tfidf_matrix)
    df['cluster'] = clusters
    
    # خطوة 6: إنشاء فهرس كامل للوثائق المجمعة
    data_iterator = document_iterator(df)
    indexer = pt.IterDictIndexer(index_path, overwrite=overwrite)
    indexer.index(data_iterator, fields=['text', 'cluster'], meta={'docno': 20, 'cluster': 2})

    print(f"Combined index built for {num_clusters} clusters.")
    