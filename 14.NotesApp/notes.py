from flask import Blueprint, request, redirect, render_template, flash, url_for
from models import Note, User
from flask_login import current_user, login_required
from app import db
import json


notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/")
@login_required
def home():
    # notes = current_user.notes.order_by(Note.created_at.desc()).all()
    notes = current_user.notes
    return render_template("home.html", notes=notes)


@notes_bp.route("/create", methods=["POST", "GET"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        note = Note(title=title, description=description, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash("Note created successfully", "success")
        return redirect(url_for("notes.home"))
    return render_template("create_note.html")


@notes_bp.route("/delete", methods=["DELETE"])
@login_required
def delete_note():
    data = json.loads(request.data)
    note_id = data["noteId"]
    note: Note = Note.query.get(note_id)

    if note.user_id != current_user.id:
        flash("You are not authorized to delete this post", "error")
        return redirect(url_for("notes.home"))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted successfully!", "success")
    return redirect(url_for("notes.home"))


@notes_bp.route("/update", methods=["PUT"])
@login_required
def update_note():
    pass
