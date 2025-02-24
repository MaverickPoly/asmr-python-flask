from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    print("Base " + request.base_url)
    print("Method " + request.method)
    print("Path " + request.path)
    name = "Some Word Here"

    return render_template("index.html", name=name)


if __name__ == '__main__':
    app.run(debug=True)
