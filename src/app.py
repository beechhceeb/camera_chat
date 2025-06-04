import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import config.logger


from flask import Flask
from main.routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)