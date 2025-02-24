from flask import Flask, render_template, request, redirect
import json, random, string


app = Flask(__name__)


def generate_short_url(length=8):
    with open("urls.json", "r") as file:
        shortened_urls = json.load(file)
    chars = string.ascii_letters + string.digits
    result = "".join([random.choice(chars) for _ in range(length)])
    while result in shortened_urls:
        result = "".join([random.choice(chars) for _ in range(length)])
    return result


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        with open("urls.json", "r") as file:
            shortened_urls = json.load(file)

        long_url = request.form.get("long_url")
        short_url = generate_short_url()
        shortened_urls[short_url] = long_url

        with open("urls.json", "w") as file:
            json.dump(shortened_urls, file)

        return render_template("index.html", short_url=request.url_root + short_url)
    return render_template("index.html")


@app.route("/<url>")
def url_route(url):
    with open("urls.json", "r") as file:
        shortened_urls = json.load(file)
    if url in shortened_urls:
        return redirect(shortened_urls[url])
    return "The requested url not found", 404


if __name__ == "__main__":
    app.run(debug=True)
