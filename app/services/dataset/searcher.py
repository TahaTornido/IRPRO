import numpy as np
from app.services.dataset.preprocessing import process_text
# import pandas as pd
import json
def search_documents(query,model):
    sanitized_query = process_text(query)
    
    try:
        # استخدام النموذج للبحث عن الوثائق
        results = model.search(sanitized_query)
        
        # استخراج قيم scores
        scores = results['score'].values
        
        # تطبيق تطبيع Min-Max مع التحقق من القيم
        min_score = np.min(scores)
        max_score = np.max(scores)
        
        if min_score == max_score:
            normalized_scores = np.zeros_like(scores)  # إذا كانت جميع القيم متساوية، اجعلها جميعاً صفر
        else:
            normalized_scores = (scores - min_score) / (max_score - min_score)
            normalized_scores = np.clip(normalized_scores, 0, 1)  # التأكد من أن القيم في النطاق [0, 1]
        
        # إضافة القيم المُطَبَّعة إلى النتائج
        results['normalized_score'] = normalized_scores
        # إرجاع 20 نتيجة فقط
        results = results.head(20)
        
        # اختيار الأعمدة المطلوبة فقط
        filtered_results = results[['docno', 'rank', 'normalized_score']]
        
        # تحويل النتائج إلى JSON
        results_json = filtered_results.to_json(orient='records')
        
        return results_json
    except Exception as e:
        print(f"Error occurred while searching for query '{query}': {e}")
        return None
    