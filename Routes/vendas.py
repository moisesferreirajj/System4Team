from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import Usuario, Cargo, db 

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route("/vendas")
def vendas():
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
    #CASO O USUÁRIO NÃO FOR DE NENHUM CARGO
    if not cargo_relacionado:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))
    cargos_permitidos = [1, 2, 3, 4, 5]
    cargo_nome = cargo_relacionado.nome
    #CASO O USUÁRIO NÃO ESTIVER DENTRO DOS CARGOS PERMITIDOS
    if cargo_relacionado.id not in cargos_permitidos:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))

    # Garantir que a imagem esteja configurada corretamente
    imagem_usuario = usuario.imagem if usuario.imagem else 'default.png'
    print(imagem_usuario)  # Verifique se o nome da imagem está correto

    return render_template('vendas.html', username=username,
                           imagem_usuario=imagem_usuario,
                           cargo=cargo_nome)
