from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "eodisxkclz"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    migrate = Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from routes import routes_bp

    app.register_blueprint(routes_bp)

    return app
