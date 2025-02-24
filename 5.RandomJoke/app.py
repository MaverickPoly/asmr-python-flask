from flask import Flask


def create_app():
    app = Flask(__name__)
    
    from joke import joke_bp

    app.register_blueprint(joke_bp)

    return app
