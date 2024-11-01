from flask import Blueprint, render_template, session, redirect, url_for, flash

painel_bp = Blueprint('painel', __name__)

@painel_bp.route("/painel")
def painel():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('start'))
    username = session['username'].capitalize()  # Tornando a primeira letra maiúscula
    return render_template('painel.html', username=username)
