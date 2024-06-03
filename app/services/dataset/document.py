import json

def get_object_by_id(json_file_path, object_id):
    """
    إرجاع الكائن من ملف JSON بناءً على رقم الـ id.

    :param json_file_path: مسار ملف الـ JSON.
    :param object_id: رقم الـ id للكائن المراد استرجاعه.
    :return: الكائن الذي يحتوي على الـ id المحدد، أو None إذا لم يتم العثور عليه.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for obj in data:
                if obj.get('id') == object_id:
                    return obj
        return None  # إذا لم يتم العثور على الكائن
    except Exception as e:
        print(f"Error occurred: {e}")
        return None