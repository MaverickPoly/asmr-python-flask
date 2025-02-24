from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import login_user, login_required, current_user, logout_user
from models import User
from app import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("auth.register"))

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        if user_email:
            flash("Account with that email already exists!", "error")
            return redirect(url_for("auth.register"))
        if user_username:
            flash("Account with that username already exists!", "error")
            return redirect(url_for("auth.register"))

        user = User(email=email, username=username)
        user.generate_password_hash(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Created account successfully", "success")
        return redirect(url_for("notes.home"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password_hash(password):
                login_user(user)
                flash("Logged in successfully", "success")
                return redirect(url_for("notes.home"))
            else:
                flash("Incorrect password", "error")
        else:
            flash("Invalid email address!", "error")
        return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("auth.login"))
