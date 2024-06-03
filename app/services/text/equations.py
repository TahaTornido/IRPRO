import re
def remove_equations(text):
    """
    This function removes text enclosed in $$...$$, $...$, or \...\. from the input text.
    
    Args:
    text (str): The input text containing equations and other enclosed text.
    
    Returns:
    str: The text with equations and other enclosed text removed.
    """
    # إزالة المعادلات المحصورة بين $$...$$
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    # إزالة المعادلات المحصورة بين $...$
    text = re.sub(r'\$.*?\$', '', text)
    # إزالة النصوص المحصورة بين \...\
    text = re.sub(r'\\.*?\\', '', text)
    return text
