from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Configs
    app.config["SECRET_KEY"] = "123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    migrate = Migrate(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from auth import auth_bp
    from blogs import blog_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    return app
