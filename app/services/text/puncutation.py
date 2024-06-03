import re
import string

def remove_punctuation(tokens):
    """
    This function takes a list of tokens and removes punctuation tokens, punctuation, and arrows from the tokens.
    It retains tokens with a '/' between words or numbers.
    
    Args:
    tokens (list): The input list of tokens.
    
    Returns:
    list: A list of tokens with punctuation and arrows removed.
    """
    # إضافة العلامات الخاصة والأسهم إلى نمط التعبير المنتظم
    additional_punctuation = "’→←↔"
    all_punctuation = string.punctuation + additional_punctuation
    punctuation_regex = re.compile(f"[{re.escape(all_punctuation)}]")

    def should_skip(token):
        # تجاوز التوكنات التي تحتوي على نص/نص أو رقم/رقم
        if re.match(r'^\w+/\w+$', token):
            return True
        if re.match(r'^\d+/\d+$', token):
            return True
        return False

    # إزالة علامات الترقيم والأسهم من كل توكن
    cleaned_tokens = [
        token if should_skip(token) else punctuation_regex.sub('', token)
        for token in tokens
    ]

    # إزالة التوكنات الفارغة التي نتجت عن إزالة جميع علامات الترقيم والأسهم
    cleaned_tokens = [token for token in cleaned_tokens if token]

    return cleaned_tokens
