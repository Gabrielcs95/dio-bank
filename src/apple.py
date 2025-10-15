from flask import Flask, url_for, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

#implementando os métodos GET e POST
#GET é usado para obter informações do servidor, enquanto POST é usado para enviar informações ao servidor
#No Flask, podemos definir rotas que respondem a esses métodos usando o decorator @app.route passano o parâmetro methods
#O método methods recebe uma lista de métodos HTTP que a rota deve responder, como ['GET', 'POST']
#Se não for especificado, o Flask irá responder apenas ao método GET por padrão
@app.route("/login, methods= ['GET', 'POST']")
def login():
    if request.method == 'POST':
        return "<h1>Login realizado com sucesso!</h1>"
    else:
        return "<h1>Por favor, faça o login.</h1>"
    

@app.route("/home")
def home_page():
    return "<h1>Olá , seja bem-vindo !</h1>"

#tipos de routes
@app.route("/user/<username>")  
def show_user_profile(username):
    return f"<h1>Perfil do usuário: {username}</h1>"

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"<h1>Postagem número: {post_id}</h1>"

#tipos com barra no final, é usado para indicar que é um caminho 
@app.route("/path/corpo/")
def show_path():
    return "<h1>Corpo do caminho</h1>"

#tipos sem barra no final, é usado para indicar que é um recurso, mesmp que coloque '/corpo' no navegador, o Flask não irá redirecionar para '/corpo/'
#e sim irá retornar o recurso diretamente
@app.route("/path/corpo")   
def show_path_no_slash():
    return "<h1>Corpo do caminho sem barra</h1>"

#=============================================#
#criando URLS com url_for
with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('home_page'))
    print(url_for('show_user_profile', username='gabriel'))

#=============================================#
#Retornando um JSON
@app.route("/json")
def return_json():
    return {
        "nome": "gabriel",
        "idade": 25,
        "cidade": "Paraiba-PB",
        "profissao": "Desenvolvedor"
    }
