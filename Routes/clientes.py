from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import Usuario, Cliente, db
from sqlalchemy import func

clientes_bp = Blueprint('clientes', __name__)

# CLIENTES, COMEÇA A LÓGICA AQUI
@clientes_bp.route("/clientes", methods=['GET', 'POST'])
def inicio():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('auth.login'))

    # VERIFICA SE A PRIMEIRA LETRA É MAIÚSCULA, SE NÃO FOR, DEIXA ELA MAIÚSCULA, AGORA SE FOR, IGNORA
    username = session['username']
    if username and username[0].islower():
        username = username.capitalize()

    # BUSCA O USUÁRIO LOGADO
    usuario = Usuario.query.filter_by(usuario=username).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('auth.login'))
    
    # CONFERE O CARGO DO USUÁRIO
    cargo_relacionado = usuario.cargo_relacionado
    if not cargo_relacionado:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))
    
    cargos_permitidos = [1, 2, 3, 4, 5]
    cargo_nome = cargo_relacionado.nome
    if cargo_relacionado.id not in cargos_permitidos:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))
    # Garantir que a imagem esteja configurada corretamente
    imagem_usuario = usuario.imagem if usuario.imagem else 'default.png'
    email = usuario.email
    
    return render_template(
        'clientes.html',
        username=username,
        imagem_usuario=imagem_usuario,
        cargo=cargo_nome,
        email=email
    )

def continuar():
    print("Passei por aqui baby - Moises!")