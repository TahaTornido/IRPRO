import re
def remove_urls(tokens):
    """
    This function takes a list of tokens and removes any URLs from the tokens.
    
    Args:
    tokens (list): The input list of tokens.
    
    Returns:
    list: A list of tokens with URLs removed.
    """
    # تعريف نمط التعبير المنتظم لإزالة الروابط
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # إزالة الروابط من كل توكن
    cleaned_tokens = [token for token in tokens if not url_regex.match(token)]
    
    return cleaned_tokens
