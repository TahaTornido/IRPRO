import json
import pandas as pd
from glob import glob
import tqdm  # إضافة مكتبة tqdm لعرض شريط التقدم
import pyterrier as pt
if not pt.started():
    pt.init()
def json_files_iterator(directory):
    files = [f"{directory}/Corpus{i}.json" for i in range(1, 3001)]
    for file_path in tqdm.tqdm(files, desc="Loading JSON files"):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    data = json.loads(line)
                    # تأكد من أن 'docno' هو من نوع string
                    data['docno'] = str(data.pop('id'))
                    yield data
# خطوة 5: تعريف Document Iterator مع التجميع
def document_iterator(df):
    for index, row in df.iterrows():
        yield {
            'docno': str(row['docno']),
            'text': row['text'],
            'cluster': str(row['cluster'])  # إضافة معلومات التجميع إلى الفهرس
        }
