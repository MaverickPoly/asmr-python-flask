from flask import Flask, request, render_template, redirect, url_for
import sqlite3

"""Using sqlite3 instead of SQLAlchemy to practice"""

app = Flask(__name__)

DATABASE = "expenses.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)
        conn.commit()


@app.route("/")
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = cursor.fetchall()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)", (amount, category, description))
            conn.commit()
        return redirect(url_for("index"))
    return render_template("add_expense.html")


@app.route("/summary")
def summary():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        summary_data = cursor.fetchall()
    print(summary_data)
    return render_template("summary.html", summary_data=summary_data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
