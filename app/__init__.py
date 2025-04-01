from flask import Flask
from app.routes import register_routes
from app.utils.logger import setup_logging

def create_app():
    app = Flask(__name__)
    setup_logging()
    register_routes(app)
    return app