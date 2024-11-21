from flask import Flask
from flask_cors import CORS
from app.routes.users import users_bp


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": ["https://driscolls-eight.vercel.app"]}})

    # Register Blueprints
    app.register_blueprint(users_bp)

    return app
