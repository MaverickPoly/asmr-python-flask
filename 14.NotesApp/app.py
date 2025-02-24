from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "bhdsxz"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"

    migrate = Migrate(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    with app.app_context():
        db.create_all()

    from auth import auth_bp
    from notes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app
