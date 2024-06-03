from app import create_app
import sys
import os
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
