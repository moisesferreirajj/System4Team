#################################
#                               #
# API - GATEWAY, ACESSAR AQUI   #
# BY: MOISES JOAO FERREIRA      #
#                               #
#################################

from flask import Flask
from config import Config
from models import db
from Routes.auth import auth_bp
from Routes.cadastro import cadastro_bp
from Routes.painel import painel_bp
from Routes.dados_painel import dados_painel_bp
from Routes.esqueceu_a_senha import esqueceu_a_senha_bp, init_mail

app = Flask(__name__)
app.config.from_object(Config)

# INICIALIZA A DB
db.init_app(app)

# Inicializa o Mail
init_mail(app)

# REGISTRA AS ROTAS
app.register_blueprint(auth_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(painel_bp)
app.register_blueprint(dados_painel_bp)
app.register_blueprint(esqueceu_a_senha_bp)

# CRIA A CONNECTION DO DB
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
