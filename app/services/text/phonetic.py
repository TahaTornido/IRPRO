import re
def remove_phonetic_notation(text):
    """
    This function removes phonetic notations enclosed in slashes (e.g., /pɜːraɪˈɒdɪk/) from the input text.
    
    Args:
    text (str): The input text containing phonetic notations.
    
    Returns:
    str: The text with phonetic notations removed.
    """
    # تعبير منتظم للبحث عن النصوص المحصورة بين /
    pattern = re.compile(r'/[^/]+/')
    
    # استبدال النصوص المطابقة بالتعبير المنتظم بنص فارغ
    cleaned_text = re.sub(pattern, '', text)
    
    return cleaned_text
