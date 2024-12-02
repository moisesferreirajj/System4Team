from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
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

    email = usuario.email    
    imagem_usuario = usuario.imagem if usuario.imagem else 'default.png'

    # CONSULTA A LISTA DE CLIENTES
    clientes = Cliente.query.all()
    
    return render_template(
        'clientes.html',
        username=username,
        imagem_usuario=imagem_usuario,
        cargo=cargo_nome,
        email=email,
        clientes=clientes
    )

@clientes_bp.route("/adicionar_cliente", methods=['POST'])
def adicionar_cliente():
    if 'username' not in session:
        return jsonify({"error": "Você precisa fazer login primeiro!"}), 401

    # PEGA OS DADOS DO MODAL
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    
    if not nome or not cpf or not endereco or not telefone or not email:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    #CRIA UM CLIENTE APÓS CERTIFICAR QUE NADA ESTÁ VAZIO
    novo_cliente = Cliente(
        nome=nome,
        cpf=cpf,
        endereco=endereco,
        telefone=telefone,
        email=email
    )

    try:
        #TENTA ADC NO BANCO
        db.session.add(novo_cliente)
        db.session.commit()
        return jsonify({"message": "Cliente adicionado com sucesso!", "cliente_id": novo_cliente.id}), 201
    except:
        #CASO AJA ERRO DE INSERT
        db.session.rollback()
        return jsonify({"error": "Erro ao adicionar cliente. Tente novamente."}), 500

@clientes_bp.route("/editar_cliente/<int:cliente_id>", methods=['POST'])
def editar_cliente(cliente_id):
    if 'username' not in session:
        return jsonify({"error": "Você precisa fazer login primeiro!"}), 401

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado!"}), 404

    # PEGA OS DADOS DO MODAL
    dados = request.form
    nome = dados.get('nome')
    email = dados.get('email')
    telefone = dados.get('telefone')
    endereco = dados.get('endereco')

    if not nome or not email or not telefone or not endereco:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    #ATUALIZA UM CLIENTE
    cliente.nome = nome
    cliente.email = email
    cliente.telefone = telefone
    cliente.endereco = endereco

    try:
        #TENTA ADC NO BANCO
        db.session.commit()
        return jsonify({"message": "Cliente atualizado com sucesso!"}), 200
    except Exception as e:
        #CASO AJA ERRO DE ATUALIZAR
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar cliente. Tente novamente. Erro: {str(e)}"}), 500

#BUSCAR ID DO CLIENTE
@clientes_bp.route("/buscar_cliente/<int:cliente_id>", methods=['GET'])
def obter_cliente(cliente_id):
    if 'username' not in session:
        return jsonify({"error": "Você precisa fazer login primeiro!"}), 401

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado!"}), 404

    #RETORNA O JSON
    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "endereco": cliente.endereco,
        "cpf": cliente.cpf
    })
