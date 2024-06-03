def convert_to_lowercase(tokens):
    """
    This function takes a list of tokens and converts all tokens to lowercase.
    
    Args:
    tokens (list): The input list of tokens.
    
    Returns:
    list: A list of tokens converted to lowercase.
    """
    lowercase_tokens = [token.lower() for token in tokens]
    return lowercase_tokens
