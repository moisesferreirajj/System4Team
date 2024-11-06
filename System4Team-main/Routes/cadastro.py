from flask import Blueprint, render_template, request, session, redirect, flash, url_for, get_flashed_messages
from models import Usuario, db
import bcrypt
import re

cadastro_bp = Blueprint('cadastro', __name__)

@cadastro_bp.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if 'username' in session:
        return redirect(url_for('painel.painel'))

    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        #VERIFICA SE O EMAIL É VALIDO
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            flash("Por favor, insira um e-mail válido.", "error")
            return redirect(url_for('cadastro.cadastrar'))

        #VERIFICA SE É COMPLEXA
        password_pattern = r'^(?=.*[A-Z])(?=(.*[0-9]){1})(?=.*[!@#$%^&*()_+\[\]{};":\\|,.<>?]).{6,}$'
        if not re.match(password_pattern, password):
            flash("A senha deve conter pelo menos 1 letra maiúscula, 1 número e 1 símbolo especial.", "danger")
            return redirect(url_for('cadastro.cadastrar'))

        #VERIFICA SE A SENHA É IGUAL
        if password != confirm_password:
            flash("As senhas não coincidem.", "error")
            return redirect(url_for('cadastro.cadastrar'))

        #VERIFICA SE EXISTE
        usuario_existente = Usuario.query.filter_by(usuario=username).first()
        email_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            flash("Usuário já existe.", "error")
            return redirect(url_for('cadastro.cadastrar'))
        
        if email_existente:
            flash("E-mail já cadastrado.", "error")
            return redirect(url_for('cadastro.cadastrar'))

        #SE NAO EXISTIR, CADASTRA
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        novo_usuario = Usuario(usuario=username, senha=hashed_password.decode('utf-8'), email=email)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")
        session['username'] = username  #LOGA NO PAINEL AUTOMATICAMENTE
        return redirect(url_for('painel.painel'))

    messages = get_flashed_messages()
    return render_template('cadastro.html', messages=messages)
