from flask import Flask


def main_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "your-secret-key"  # Needed for Flask sessions

    # Blueprints registration
    from app.views.auth.user_auth import auth_bp
    from app.views.home.land import home_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

    return app
