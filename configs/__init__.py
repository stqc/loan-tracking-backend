from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from configs.config import configs

db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(configs)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)

    from .routes.user_login_sign_up import user_login_sign_up
    from .routes.loan_interactions import loan_interactions

    app.register_blueprint(user_login_sign_up, url_prefix='/api')
    app.register_blueprint(loan_interactions, url_prefix='/api/loans')

    with app.app_context():
        db.create_all()

    return app
