# Importa a classe Blueprint, o objeto request e o HTTPStatus do Flask
from flask import Blueprint, request
from ..app import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from ..utils import requires_role

# Cria a instância do blueprints
# "user" ->> nome do blueprint
# "__name__" ->> nome de importação do módulo, que pega o caminho controllers.user
# "url_prefix="/users"" ->> o que fica no endereço do navegador.
# obs: o termo "userS" está no padrão RESTful, ou seja, no plural

app = Blueprint("user", __name__, url_prefix="/userS")

# Esta função será usada para criar um novo usuário via POST
# Ela não precisa estar diretamente ligada a uma rota, pois será chamada por handle_user
def create_user():
    # O request.json retorna o corpo da requisição em um dicionário Python
    data = request.json
    # Cria uma nova instância da classe User com o username fornecido
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"],
    )
    # Adiciona a nova instância à sessão do banco de dados
    db.session.add(user)
    # Confirma a transação, salvando o novo usuário no banco de dados
    db.session.commit()

#METODO PARA LER (READ) OS USUARIOS
#USA-SE O scalars PARA 
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role.id,
                "name": user.role.name
            }
        }
        for user in users
    ]


# Esta é a função principal que gerencia a rota e os métodos
# Ela agora lida com os métodos GET e POST
@app.route('/', methods=["GET", "POST"])
@jwt_required()  # Protege a rota, exigindo um token JWT válido
def handle_user():

    # Verifica se o usuário tem a role "admin"
    requires_role("admin")  

    # Verifica o tipo de método HTTP da requisição
    if request.method == "POST":
        # Se for POST, chama a função create_user para criar o usuário
        create_user()
        # Retorna a mensagem
        # 
        #  de sucesso com o status code 201 (CREATED)
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        # Se for GET ou qualquer outro método, retorna a mensagem
        return {"users": _list_users()}

#METODO LISTAGEM POR (ID)
@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user_id,
        "username": user.username,
    } 

#MOTODO DE UPDATE

@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
            db.session.commit()
    return{
        "id": user.id,
        "username": user.username,
    }
#METODO DE DELETE
@app.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT


