from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from models import Usuario, Funcionario, db
from sqlalchemy import func

funcionarios_bp = Blueprint('funcionarios', __name__)

#FUNCIONÁRIOS, APENAS RETORNA TEMPLATE
@funcionarios_bp.route("/funcionarios", methods=['GET', 'POST'])
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

    email = usuario.email    
    imagem_usuario = usuario.imagem if usuario.imagem else 'default.png'

    # CONSULTA A LISTA DE FUNCIONÁRIOS
    funcionarios = Funcionario.query.all()
    
    return render_template(
        'funcionarios.html',
        username=username,
        imagem_usuario=imagem_usuario,
        cargo=cargo_nome,
        email=email,
        funcionarios=funcionarios
    )

#ADICIONAR FUNCIONÁRIOS - ROUTE POST
@funcionarios_bp.route("/json/adicionar_funcionario", methods=['POST'])
def adicionar_funcionario():
    if 'username' not in session:
        return jsonify({"error": "Você precisa fazer login primeiro!"}), 401

    # PEGA OS DADOS DO MODAL
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    
    if not nome or not telefone or not email:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    #CRIA UM FUNCIONÁRIO APÓS CERTIFICAR QUE NADA ESTÁ VAZIO
    novo_funcionario = Funcionario(
        nome=nome,
        telefone=telefone,
        email=email
    )

    try:
        #TENTA ADICIONAR NO BANCO
        db.session.add(novo_funcionario)
        db.session.commit()
        return jsonify({"message": "Funcionário adicionado com sucesso!", "funcionario_id": novo_funcionario.id}), 201
    except:
        #CASO AJA ERRO DE INSERT
        db.session.rollback()
        return jsonify({"error": "Erro ao adicionar funcionário. Tente novamente."}), 500

#EDITAR FUNCIONÁRIOS - ROUTE POST
@funcionarios_bp.route("/json/editar-funcionario/<int:funcionario_id>", methods=['POST'])
def editar_funcionario(funcionario_id):
    if 'username' not in session:
        return jsonify({"error": "Você precisa fazer login primeiro!"}), 401

    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"error": "Funcionário não encontrado!"}), 404

    # PEGA OS DADOS DO MODAL
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    if not nome or not email or not telefone:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    #ATUALIZA UM FUNCIONÁRIO
    funcionario.nome = nome
    funcionario.email = email
    funcionario.telefone = telefone

    try:
        #TENTA ADICIONAR NO BANCO
        db.session.commit()
        return jsonify({"message": "Funcionário editado com sucesso!"}), 200
    except:
        #CASO AJA ERRO DE ATUALIZAR
        db.session.rollback()
        return jsonify({"error": "Erro ao editar funcionário. Tente novamente."}), 500

#BUSCAR ID DO FUNCIONÁRIO - ROUTE GET
@funcionarios_bp.route("/json/buscar-funcionario/<int:funcionario_id>", methods=['GET'])
def obter_funcionario(funcionario_id):
    if 'username' not in session:
        return jsonify({"error": "Você precisa fazer login primeiro!"}), 401

    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"error": "Funcionário não encontrado!"}), 404

    #RETORNA O JSON
    return jsonify({
        "id": funcionario.id,
        "nome": funcionario.nome,
        "cargo": funcionario.cargo,
        "email": funcionario.email,
        "telefone": funcionario.telefone,
        "id_empresa": funcionario.id_empresa
    })
