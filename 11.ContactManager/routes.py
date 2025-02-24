from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Contact
from app import db


routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")

        contact = Contact(last_name=last_name, first_name=first_name, email=email)
        db.session.add(contact)
        db.session.commit()
        flash("Created contact successfully!")
        return redirect(url_for("routes.home"))

    contacts = Contact.query.order_by(Contact.id.desc()).all()
    return render_template("index.html", contacts=contacts)


@routes_bp.route("/update", methods=["POST"])
def update():
    pass


@routes_bp.route("/delete", methods=["DELETE"])
def delete():
    pass

