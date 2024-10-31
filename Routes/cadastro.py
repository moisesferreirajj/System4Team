from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Usuario, db
import bcrypt

cadastro_bp = Blueprint('cadastro', __name__)

@cadastro_bp.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash("As senhas não correspondem.", "error")
            return redirect(url_for('cadastro.cadastrar'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        if Usuario.query.filter_by(usuario=username).first():
            flash("Usuário já existe.", "error")
        else:
            novo_usuario = Usuario(usuario=username, senha=hashed_password.decode('utf-8'), email=email)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for('auth.login'))
    return render_template('cadastro.html')
