import os
import json
import signal
import atexit
from tqdm import tqdm

import os
import json
import signal
import atexit
from tqdm import tqdm
from app.services.dataset.preprocessing import process_text

# متغير لتتبع الملف الأخير الذي يتم معالجته
current_file = None

def handle_exit():
    if current_file and os.path.exists(current_file):
        print(f"حذف الملف الأخير المكتمل: {current_file}")
        os.remove(current_file)

# تسجيل دالة handle_exit ليتم استدعاؤها عند إنهاء البرنامج
atexit.register(handle_exit)

# تسجيل دالة handle_exit ليتم استدعاؤها عند استقبال إشارة إنهاء البرنامج
signal.signal(signal.SIGINT, lambda sig, frame: handle_exit() or exit(1))
signal.signal(signal.SIGTERM, lambda sig, frame: handle_exit() or exit(1))

# الدالة الرئيسية لمعالجة الملفات
def process_files(input_folder, output_folder, files):
    global current_file
    os.makedirs(output_folder, exist_ok=True)
    
    # جمع أسماء الملفات
    file_names = [f'corpus{i}.json' for i in range(1, files + 1)]
    
    # تحقق من آخر ملف مكتمل
    last_processed_file = None
    for file_name in reversed(file_names):
        if os.path.exists(os.path.join(output_folder, file_name)):
            last_processed_file = file_name
            break
    
    # إذا وجد آخر ملف مكتمل، حذفه
    if last_processed_file:
        print(f"حذف الملف الأخير المكتمل: {last_processed_file}")
        os.remove(os.path.join(output_folder, last_processed_file))
        # استئناف المعالجة من الملف الذي تم حذفه
        start_index = file_names.index(last_processed_file)
    else:
        start_index = 0

    # قراءة وتنظيف البيانات من ملفات corpus
    for file_name in tqdm(file_names[start_index:], desc="Processing files"):
        file_path = os.path.join(input_folder, file_name)
        try:
            cleaned_data = []
            
            # قراءة الملف كسطور نصية
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = json.loads(line)
                    if 'text' in entry:
                        entry['text'] = process_text(entry['text'])
                    cleaned_data.append(entry)
            
            # تحديد الملف الحالي
            current_file = os.path.join(output_folder, file_name)
            
            # حفظ البيانات النظيفة إلى ملف جديد بنفس الاسم في مجلد الوجهة
            with open(current_file, 'w', encoding='utf-8') as f:
                for entry in cleaned_data:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
        except json.JSONDecodeError:
            print(f"الملف {file_name} يحتوي على أخطاء في الترميز.")
        except Exception as e:
            print(f"خطأ في معالجة الملف {file_name}: {e}")

    # إعادة تعيين current_file عند اكتمال المعالجة بنجاح
    current_file = None
    print("تمت عملية تنظيف جميع الملفات بنجاح.")
    