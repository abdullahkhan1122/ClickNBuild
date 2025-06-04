from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy globally

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')  # Load your DB and app config

    db.init_app(app)  # Initialize database with app

    # Import blueprints inside create_app
    from app.routes.client_routes import client_bp
    from app.routes.builder_routes import builder_bp
    from app.routes.auth_routes import auth_bp  

    # Register blueprints
    app.register_blueprint(client_bp)
    app.register_blueprint(builder_bp)
    app.register_blueprint(auth_bp)

    return app
