from flask import Blueprint, render_template, session, redirect, url_for, flash

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

    return render_template('painel.html', username=username)
