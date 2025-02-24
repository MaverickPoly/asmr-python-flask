from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ejwdksla"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    migrate = Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from todos import todos_bp

    app.register_blueprint(todos_bp)

    return app

