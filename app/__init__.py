from flask import Flask
from flask_cors import CORS
from app.routes.users import users_bp


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:5173", "https://orm-react.vercel.app"]
            }
        },
    )

    # Users Home
    @app.route("/")
    def home():
        return {"message": "Welcome to Python REST-Full ORM Supabase API"}, 200

    # Register Blueprints
    app.register_blueprint(users_bp)

    return app
