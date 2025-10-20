import os  # Para manipular arquivos e pastas do sistema

from flask import Flask, current_app  # Flask cria a aplicação; current_app acessa o app no contexto
from flask_sqlalchemy import SQLAlchemy  # Integração do SQLAlchemy com Flask
from sqlalchemy.orm import DeclarativeBase  # Base para criar models no SQLAlchemy 2.0
import click  # Biblioteca para criar comandos CLI (terminal)
from datetime import datetime
import sqlalchemy as sa 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_migrate import Migrate
#usa o flask_migrate para gerenciar migrações de banco de dados
from flask_jwt_extended import JWTManager



# =========================
# Classe Base para os Models
# =========================
class Base(DeclarativeBase):
    pass  # Classe base vazia que será herdada por todos os modelos


# =========================
# Instância do SQLAlchemy
# =========================
db = SQLAlchemy(model_class=Base)  # db será usado para criar tabelas e gerenciar o banco

migrate = Migrate()  # Instância do Flask-Migrate para gerenciar migrações
jwt = JWTManager()  # Instância do JWTManager para gerenciar autenticação JWT

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"  


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column( sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)   
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body : Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r} )"
    

# =========================
# Comando CLI: Inicializa o banco
# =========================
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db  # Usando a variável db definida fora da função
    # Entrando no contexto do app para usar o banco
    with current_app.app_context():
        db.create_all()  # Cria todas as tabelas definidas nos models
    click.echo('Initialized the database.')  # Mensagem de confirmação no terminal


# =========================
# Application Factory
# =========================
def create_app(test_config=None):
    """
    Cria e configura a aplicação Flask.
    Recebe test_config se quiser rodar com configuração de teste.
    """
    # Cria a aplicação Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configurações básicas
    app.config.from_mapping(
        SECRET_KEY='dev',  # Segurança (cookies, sessão)
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATA_BASE_URL"),  # Banco SQLite
        DEBUG=True,  # Ativa modo debug (erros detalhados + recarregamento automático)
        JWT_SECRET_KEY='super-secret',  # Chave secreta para JWT
    )

    # Carrega configurações extras, se houver
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)  # Tenta carregar config externa
    else:
        app.config.from_mapping(test_config)  # Usa config de teste

    # Garante que a pasta instance/ exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # Se já existir, ignora

    # Registra o comando CLI init-db
    app.cli.add_command(init_db_command)

    # Inicializa o SQLAlchemy com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)  # Configura migrações de banco de dados
    jwt.init_app(app)  # Configura JWT com a aplicação

    # register blueprints usando imports relativos (quando o pacote for importado como `src`)
    from .controllers import user, role, auth

    app.register_blueprint(role.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(user.app)

    return app  # Retorna a instância do app pronta para rodar
