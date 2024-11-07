# Em painel.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import Usuario, Cargo, db 

painel_bp = Blueprint('painel', __name__)

@painel_bp.route("/painel")
def painel():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('auth.login'))
    #VERIFICA SE A PRIMEIRA LETRA É MAIUSCULA, SE NAO FOR, DEIXA ELA MAIUSCULA, AGORA SE FOR, IGNORA
    username = session['username']
    if username and username[0].islower():
        username = username.capitalize()
    #BUSCA O USUÁRIO LOGADO
    usuario = Usuario.query.filter_by(usuario=username).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('auth.login'))
    #CONFERE O CARGO DO USUÁRIO
    cargo_relacionado = usuario.cargo_relacionado
    cargos_permitidos = [1, 2, 3, 4, 5]
    cargo_nome = cargo_relacionado.nome
    if cargo_relacionado.id not in cargos_permitidos:
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))

    return render_template('painel.html', username=username, cargo=cargo_nome)
