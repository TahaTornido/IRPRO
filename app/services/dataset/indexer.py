import json
import pandas as pd
from glob import glob
import tqdm  
import os
from app.services.dataset.file_reader import json_files_iterator
import pyterrier as pt
if not pt.started():
    pt.init()
def create_index(data_path, index_path, fields=['text'], meta_field_length={'docno': '20'}, overwrite=True):
    """
    Create an index using IterDictIndexer from the specified data path and save it to the specified index path.

    Parameters:
    - data_path (str): The path to the directory containing JSON files.
    - index_path (str): The path where the index will be saved.
    - fields (list): List of fields to index.
    - meta_field_length (dict): Metadata fields with their respective lengths.
    - overwrite (bool): Whether to overwrite the existing index.

    Returns:
    - index_ref: Reference to the created index.
    """
    # Create a data iterator from the JSON files in the specified directory
    data_iterator = json_files_iterator(data_path)
    
    # Create the index using IterDictIndexer
    indexer = pt.IterDictIndexer(index_path, overwrite=overwrite)
    
    # Index the data iterator and return the reference to the index
    index_ref = indexer.index(data_iterator, fields=fields, meta=meta_field_length)
    
    return index_ref
