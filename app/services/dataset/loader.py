import pyterrier as pt

def load_index_and_create_tfidf_model(index_path):
    """
    Load an index from the specified path and create a TF-IDF model using the loaded index.

    Parameters:
    - index_path (str): The path where the index is saved.

    Returns:
    - tfidf_model: The TF-IDF model created using the loaded index.
    """
    # Load the index from the specified path
    index_load = pt.IndexFactory.of(index_path)
    
    # Create a TF-IDF model using the loaded index
    tfidf_model = pt.BatchRetrieve(index_load, wmodel="TF_IDF")
    
    return tfidf_model
