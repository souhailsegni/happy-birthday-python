
from flask import Flask
from config import DevelopmentConfig
from models import db
from routes import create_api_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    api = create_api_blueprint()
    app.register_blueprint(api)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
