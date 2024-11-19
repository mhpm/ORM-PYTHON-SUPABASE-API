from flask import Flask
from app.routes.users import users_bp


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(users_bp)

    return app
