# Em auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Usuario, db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def passlogin():
    if 'username' in session:
        return redirect(url_for('painel.painel'))
    return render_template('index.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('painel.painel'))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        user = Usuario.query.filter_by(usuario=username).first()
        #CHECK PARA VER SE A SENHA ESTÁ NO MODO BCRYPT
        if user and bcrypt.checkpw(password, user.senha.encode('utf-8')):
            session['username'] = username
            return redirect(url_for('painel.painel'))
        
        flash('Usuário ou senha inválidos!', 'error')
    
    return render_template('index.html')

@auth_bp.route("/logout")
def logout():
    session.pop('username', None)
    flash('Você saiu com sucesso!')
    return redirect(url_for('auth.login'))
