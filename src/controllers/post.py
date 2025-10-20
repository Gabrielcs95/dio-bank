from flask import Blueprint, request
from ..app import db, Post
from http import HTTPStatus

app = Blueprint("post", __name__, url_prefix="/posts")

@app.route("/", methods=["GET", "POST"])
def list_posts():
    posts = db.session.execute(db.select(Post)).scalars().all()
    #aqui sera os retornos dos posts
    return [
        {"id": post.id, "title": post.title, "content": post.content}
        for post in posts
    ], HTTPStatus.OK


