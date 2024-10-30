from flask import Flask, url_for, render_template, request, redirect, flash, session, jsonify
import bcrypt

# INICIALIZA
app = Flask(__name__)
app.secret_key = 'System4Team-MoisesAPI2024'

# USUARIOS COM SENHA CRIPTOGRAFADA EM VETOR
usuarios = [
    {
        "username": "moises",
        "password": bcrypt.hashpw("teste".encode('utf-8'), bcrypt.gensalt())
    },
    {
        "username": "igor",
        "password": bcrypt.hashpw("teste".encode('utf-8'), bcrypt.gensalt())
    },
    {
        "username": "mark",
        "password": bcrypt.hashpw("teste".encode('utf-8'), bcrypt.gensalt())
    }
]

# ROTAS
@app.route("/")
def start():
    return render_template('index.html')

@app.route("/painel")
def painel():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('start'))
    return render_template('painel.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    for user in usuarios:
        if user['username'] == username and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('painel'))
    return render_template('index.html', error='Usuário ou senha inválidos!')

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('Você saiu com sucesso!')
    return redirect(url_for('start'))

@app.route("/dados_painel")
def dados_painel():
    # Simular dados do painel
    dados = {
        "vendas": '5000',
        "pedidos": '30',
        "inscricoes": '50',
        "receita": '150',
        "vendas_mensais": ['200', '300', '250', '400', '350', '500'],
        "despesas_mensais": ['150', '200', '100', '250', '200', '300'],
    }
    return jsonify(dados)

@app.route("/esqueceu-a-senha")
def senha():
    print("Passou aki")
    return None

# INICIALIZA O SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)
