from flask import Flask, render_template, request, redirect, session, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "rdjncsx,z"

chat_messages = []


@app.route("/")
def home():
    return redirect(url_for("chat"))


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        username = session.get("username", "Anonymous")
        message = request.form.get("message")
        if message:
            chat_messages.append({"username": username, "message": message})
        return redirect(url_for("chat"))
    return render_template("chat.html", messages=chat_messages, username=session.get("username", "Anonymous"))


@app.route("/set_username", methods=["GET", "POST"])
def set_username():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        return redirect(url_for("chat"))
    return render_template("set_username.html")


@app.route("/clear")
def clear_chat():
    global chat_messages
    chat_messages = []
    return redirect(url_for("chat"))


if __name__ == '__main__':
    app.run(debug=True)
