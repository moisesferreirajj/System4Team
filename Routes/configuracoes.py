from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import Usuario, db
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/images/profile'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#VERIFICA SE A EXTENSÃO É PERMITIDA
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

configuracoes_bp = Blueprint('configuracoes', __name__)

# CONFIG, COMEÇA A LÓGICA AQUI
@configuracoes_bp.route("/configuracoes", methods=['GET', 'POST'])
def configuracoes():
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
        'configuracoes.html',
        username=username,
        imagem_usuario=imagem_usuario,
        cargo=cargo_nome,
        email=email
    )

@configuracoes_bp.route("/alterar_imagem", methods=['POST'])
def alterar_imagem():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.filter_by(usuario=session['username']).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('auth.login'))

    #VERIFICA SE O USUARIO ENVIOU A IMAGEM
    if 'imagem' not in request.files:
        flash('Nenhuma imagem foi selecionada!')
        return redirect(url_for('configuracoes.configuracoes'))

    imagem = request.files['imagem']

    #SE ELE NÃO SELECIONOU NENHUMA IMAGEM
    if imagem.filename == '':
        flash('Nenhuma imagem foi selecionada!')
        return redirect(url_for('configuracoes.configuracoes'))

    #SE O ARQUIVO FOR VALIDO ELE FAZ O UPLOAD
    if imagem and allowed_file(imagem.filename):
        filename = secure_filename(imagem.filename)  #GARANTE QUE O ARQUIVO SEJA SEGURO
        caminho_imagem = os.path.join(UPLOAD_FOLDER, filename)

        #SALVE O ARQUIVO NO SISTEMA DO SERVIDOR
        imagem.save(caminho_imagem)

        #ATUALIZA A IMAGEM NO BANCO
        usuario.imagem = filename
        db.session.commit()

        flash('Imagem de perfil alterada com sucesso!')
    else:
        flash('Tipo de arquivo inválido! Apenas imagens PNG, JPG, JPEG e GIF são permitidas.')

    return redirect(url_for('configuracoes.configuracoes'))