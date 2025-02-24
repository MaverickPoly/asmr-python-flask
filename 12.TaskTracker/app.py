from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SECRET_KEY HERE"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    migrate = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import register_routes
    register_routes(app)

    return app
