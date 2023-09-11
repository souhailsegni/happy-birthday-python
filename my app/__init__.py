from flask import Flask
from .models import db
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import app  # Import your routes module
        db.create_all()

    return app
