from flask import Flask, request, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from models import User, Task

"""
Logging in Without using Flask_Login module, instead using sessions naturally
"""


def register_routes(app: Flask):
    @app.route("/")
    def index():
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            tasks = Task.query.filter_by(user_id=user.id).order_by(Task.deadline).all()
            return render_template("index.html", tasks=tasks, user=user)
        return redirect(url_for("login"))


    @app.route("/register", methods=["POST", "GET"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("Passwords do not match!", "danger")
                return redirect(url_for("register"))

            if User.query.filter_by(username=username).first():
                flash("Username already exists!", "danger")
                return redirect(url_for("register"))

            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")


    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                flash("Login successful!", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid credentials!", "danger")
        return render_template("login.html")

    @app.route("/logout", methods=["POST", "GET"])
    def logout():
        if "user_id" in session:
            session.pop("user_id", None)
            flash("Logged out successfully!", "success")
            return redirect(url_for("login"))

    @app.route("/add", methods=["POST", "GET"])
    def add_task():
        if "user_id" not in session:
            return redirect(url_for("login"))

        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            deadline = request.form.get("deadline")
            priority = request.form.get("priority")

            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None

            new_task = Task(
                title=title,
                description=description,
                deadline=deadline_dt,
                priority=priority,
                user_id=session["user_id"]
            )
            db.session.add(new_task)
            db.session.commit()
            flash("New task added successfully!", "success")
            return redirect(url_for("index"))\

        return render_template("add_task.html")


    @app.route("/delete/<int:task_id>")
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != session.get("user_id"):
            flash("You are not authorized to do this!", "danger")
            return redirect(url_for("index"))

        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully!", "success")
        return redirect(url_for("index"))

    @app.route("/complete/<int:task_id>")
    def complete_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != session.get("user_id"):
            flash("Unauthorized action!", "danger")
            return redirect(url_for("index"))
        task.completed = not task.completed
        db.session.commit()
        flash("Task updated successfully", "success")
        return redirect(url_for("index"))


