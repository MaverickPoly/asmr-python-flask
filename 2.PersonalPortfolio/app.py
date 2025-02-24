from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
app.secret_key = ""
app.config["secret_key"] = "SECRET_KEY"


@app.route("/")
def index():
    skills = [
        {"title": "Python", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/python.png"},
        {"title": "JavaScript", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/js.png"},
        {"title": "Dart", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/dart.png"},
        {"title": "Java", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/java.png"},
        {"title": "C", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/c.png"},
        {"title": "C++", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/cpp.png"},
        {"title": "Godot Engine", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/gd.png"},
        {"title": "PHP", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/php.png"},
        {"title": "Kotlin", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/kotlin.png"},
        {"title": "GoLang", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/python.png"},
        {"title": "Rust", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/python.png"},
        {"title": "Ruby", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/python.png"},
        {"title": "R Lang", "description": "Lorem ipsum dolor sit amet, consectetur adip", "image": "images/python.png"},
    ]
    return render_template("index.html", skills=skills)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=True)
