import re
def sanitize_query(query):
    # إزالة الأحرف غير المسموح بها
    query = re.sub(r"[^a-zA-Z0-9\s]", " ", query)  # استبدال الأحرف غير المسموح بها بمسافات
    query = query.strip()  # إزالة المسافات الزائدة في البداية والنهاية
    query = re.sub(r"\s+", " ", query)  # استبدال المسافات المتعددة بمسافة واحدة
    return query
