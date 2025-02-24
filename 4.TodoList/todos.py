from flask import Blueprint, request, render_template, flash, redirect, url_for
from models import Todo
from todo_app import db


todos_bp = Blueprint("todos", __name__)


@todos_bp.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        title = request.form.get("title")

        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
        flash("Created new todo successfully!")
        return redirect(url_for("todos.home"))

    elif request.method == "GET":
        todos = Todo.query.order_by(Todo.id.desc()).all()
        return render_template("todos.html", todos=todos)
    

@todos_bp.route("/update", methods=["POST"])
def update_todo():
    data = request.get_json()
    todo_id = data.get("id")
    completed = data.get("completed")

    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = completed
        db.session.commit()
        return {"success": True}, 200
    else:
        return {"success": False, "message": "Todo not found"}, 404
