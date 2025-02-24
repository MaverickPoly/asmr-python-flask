import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import os
from app import db
from werkzeug.utils import secure_filename
from models import User, Blog

blog_bp = Blueprint("blogs", __name__)


@blog_bp.route("/")
def blogs_list():
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template("blogs/blogs_list.html", blogs=blogs)


@blog_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_blog():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files.get("image")

        current_date = datetime.now()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")

        base_upload_path = "static/uploads"
        upload_path = os.path.join(base_upload_path, year, month, day)
        os.makedirs(upload_path, exist_ok=True)

        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_path, filename)
        image.save(image_path)

        relative_path = "/".join([year, month, day]) + "/" + filename
        blog = Blog(title=title, content=content, image=relative_path, user_id=current_user.id)
        db.session.add(blog)
        db.session.commit()
        flash("Created blog successfully!", "success")
        return redirect(url_for("blogs.blogs_list"))

    return render_template("blogs/upload_blog.html")


@blog_bp.route("/delete", methods=["DELETE"])
@login_required
def delete_post():
    data = json.loads(request.data)
    blog_id = data["blogId"]
    blog: Blog = Blog.query.get(blog_id)

    if blog.user_id != current_user.id:
        flash("You are not authorized to delete this blog.", "error")
        return redirect(url_for("blogs.blogs_list"))

    image_path = os.path.join("static/uploads", blog.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted successfully!", "success")
    return redirect(url_for("blogs.blogs_list"))

