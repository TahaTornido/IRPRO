from flask import Blueprint, render_template, request, jsonify,Response
import pyterrier as pt
import app.services.dataset.loader as dl
import app.services.dataset.searcher as ds
import app.services.dataset.preprocessing as pr
import pandas as pd
from constants import LOTTE_INDEX,QOURA_INDEX,LOTTE_INDEX_CLUSTER,QOURA_INDEX_CLUSTER,LOG_FILE,QUERY_REFIN_FOLDER,FILE_PATHS_QUER,LOTTE,QOURA
from app.services.query_refi.query_handler import QueryHandler
import json
from app.services.dataset.document import get_object_by_id


if not pt.started():
    pt.init()
    
    
processor = QueryHandler(QUERY_REFIN_FOLDER, LOG_FILE)
processor.vectorizer, processor.tfidf_matrix, processor.queries = processor.load_model_and_matrix()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
@main.route('/get_document', methods=['POST'])
def get_document():
    data = request.get_json()
    id = data['id']
    dataset_name = data['dataset_name']
    if dataset_name == 'lotte':
       document=get_object_by_id(id,LOTTE)  
       print(document)
    elif dataset_name == 'qoura':
       document=get_object_by_id(id,QOURA)
    result_json = json.dumps(document, ensure_ascii=False)
    response = Response(result_json, mimetype='application/json')
    return response
@main.route('/correct_query', methods=['POST'])
def correct_query():
    data = request.get_json()
    query = data['query']
    correct_text=processor.correct_spelling_and_grammar(query)
    result = {
            "corrected_text": correct_text,
        }
    result_json = json.dumps(result, ensure_ascii=False)
    response = Response(result_json, mimetype='application/json')
    return response
@main.route('/suggest_query', methods=['POST'])
def suggest_query():
    data = request.get_json()
    query = data['query']
    correct_text=processor.get_suggestions_tfidf(query)
    result = {
            "suggestions": correct_text,
        }
    result_json = json.dumps(correct_text, ensure_ascii=False)
    response = Response(result_json, mimetype='application/json')
    return response
@main.route('/search', methods=['POST'])
def search():
    data = request.get_json()

    if 'query' not in data or 'dataset_name' not in data or 'is_cluster' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    query = data['query']
    dataset_name = data['dataset_name']
    is_cluster = data['is_cluster']
    result=None
    if dataset_name == 'lotte':
        index=LOTTE_INDEX
        model=dl.load_index_and_create_tfidf_model(index)
        result=ds.search_documents(query,model)
        response = Response(result, mimetype='application/json')

        if is_cluster ==True:
            index=LOTTE_INDEX_CLUSTER
            model=dl.load_index_and_create_tfidf_model(index)
            result=ds.search_documents(query,model)
            response = Response(result, mimetype='application/json')
        else:
            # تنفيذ البحث في البيانات غير المجمعة
            result 
    elif dataset_name == 'qoura':
        index=QOURA_INDEX
        model=dl.load_index_and_create_tfidf_model(index)
        result=ds.search_documents(query,model)
        response = Response(result, mimetype='application/json')

        if is_cluster ==True:
            index=QOURA_INDEX_CLUSTER
            model=dl.load_index_and_create_tfidf_model(index)
            result=ds.search_documents(query,model)
            response = Response(result, mimetype='application/json')
        else:
            # تنفيذ البحث في البيانات غير المجمعة
            result 
    else:
        return jsonify({"error": "Invalid dataset_name"}), 400
    
    return response