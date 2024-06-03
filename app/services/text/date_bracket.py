import re
from dateutil import parser
from dateutil.parser import ParserError
def process_and_standardize_dates_brackets(tokens):
    """
    This function takes a list of tokens, processes and standardizes any dates found
    within the tokens while keeping all numbers as they are.

    Args:
    tokens (list): The input list of tokens.

    Returns:
    list: A list of processed tokens with dates standardized.
    """
    processed_tokens = []

    for token in tokens:
        # إزالة الأقواس
        token = re.sub(r'[()]', '', token)
        processed_tokens.append(token)
        # الاحتفاظ بالأرقام بغض النظر عن طولها
        if re.match(r'^\d+$', token):
            processed_tokens.append(token)
        else:
            # محاولة تحويل التوكن إلى تاريخ وتنسيقه
            try:
                parsed_date = parser.parse(token, fuzzy=False)
                # تحويل التاريخ إلى تنسيق 'YYYY-MM-DD'
                standardized_date = parsed_date.strftime('%Y-%m-%d')
                processed_tokens.append(standardized_date)
            except (ParserError, ValueError, OverflowError):
                # إذا لم يكن تواريخًا، قم بإضافة الكلمة كما هي
                processed_tokens.append(token)

    return processed_tokens
