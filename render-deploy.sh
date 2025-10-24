#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
set -e

# Rodar as migrações do banco de dados
# Note os dois traços: --app
# E use o mesmo caminho do gunicorn: src.wsgi:app
poetry run flask --app src.wsgi:app db upgrade