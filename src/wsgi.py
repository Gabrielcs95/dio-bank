from .app import create_app

# Cria a aplicação usando a application factory.
# Import relativo necessário porque este módulo está dentro do pacote `src`.
app = create_app()