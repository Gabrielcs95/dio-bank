# Importa a classe Blueprint, o objeto request e o HTTPStatus do Flask
from flask import Blueprint, request
from app import db, Role
from http import HTTPStatus

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route('/', methods=["POST"])
def create_role():
    data = request.json
    role = Role(
        name=data.get("name")
    )
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED 