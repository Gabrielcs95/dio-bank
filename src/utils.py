from flask_jwt_extended import get_jwt_identity
from functools import wraps
from .app import User, db
from http import HTTPStatus
  
def requires_role(role_name):
    def decorator(f):
          @wraps(f)
          def wrapper(*args, **kwargs):
              user_id = get_jwt_identity()  # Obtém o ID do usuário a partir do token JWT
              user = db.get_or_404(User, user_id)  # Busca o usuário no banco de dados ou retorna 404 se não encontrado
              if user.role.name != role_name:  # Verifica se o usuário tem a role "admin"
                  return {"msg": "User dont have access!"}, HTTPStatus.FORBIDDEN
              return f(*args, **kwargs)
          return wrapper
    return decorator