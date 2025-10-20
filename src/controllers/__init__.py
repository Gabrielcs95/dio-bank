"""Pacote controllers que expõe os blueprints.

Este arquivo torna `src.controllers` um pacote e permite importações relativas
quando a aplicação é carregada por gunicorn/WSGI.
"""

from .user import app as user_app
from .role import app as role_app
from .auth import app as auth_app

__all__ = ["user_app", "role_app", "auth_app"]
