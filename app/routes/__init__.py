# from flask import Flask
# from app.routes.builder_routes import builder_bp
# from app.routes.client_routes import client_bp
# from app.routes.auth_routes import auth_bp

# def create_app():
#     app = Flask(__name__)

#     app.secret_key = '123'

#     app.config.from_object('config')

#     # Register Blueprints
#     app.register_blueprint(client_bp)
#     app.register_blueprint(builder_bp)
#     app.register_blueprint(auth_bp)

#     return app
