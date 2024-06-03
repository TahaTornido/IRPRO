from flask import Flask

def create_app():
    # إنشاء كائن التطبيق
    app = Flask(__name__)

    # تحميل الإعدادات من ملف الإعدادات الافتراضي
    app.config.from_object('config.Config')

    # استيراد وتسجيل blueprints
    from app.controllers.main_controller import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
