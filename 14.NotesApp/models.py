from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    notes = db.relationship("Note", backref="note")

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("user_notes", lazy=True))


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(int(user_id))
