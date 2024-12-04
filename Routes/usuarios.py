from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from models import Usuario, Cargo, db 

usuarios_bp = Blueprint('Usuarios', __name__)

@usuarios_bp.route("/usuarios")
def usuarios():
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
    if not cargo_relacionado:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))
    cargos_permitidos = [1, 2, 3, 4, 5]
    #CASO O USUÁRIO NÃO FOR DE NENHUM CARGO OU NAO FOR CARGO PERMITIDO
    if cargo_relacionado.id not in cargos_permitidos:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))
    
    #BUSCA TODOS CLIENTES NO USUARIO
    usuarios_lista = Usuario.query.all()
    imagem_usuario = usuario.imagem if usuario.imagem else 'default.png'
    return render_template('usuarios.html', 
                           usuarios=usuarios_lista, 
                           username=username, 
                           cargo=cargo_relacionado.nome, 
                           imagem_usuario=imagem_usuario)

#BUSCAR USUARIO - ROUTE GET
@usuarios_bp.route("/json/buscar-usuario/<int:id>", methods=["GET"])
def get_usuario_data(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado!"}), 404

    return jsonify({
        "id": usuario.id,
        "username": usuario.usuario,
        "email": usuario.email,
        "cargo": usuario.cargo,
        "funcionario": usuario.id_funcionario
    })

# EDITAR USUÁRIO - ROUTE POST
@usuarios_bp.route("/json/editar-usuario/<int:id>", methods=["POST"])
def editar_usuario(id):
    if 'username' not in session:
        return jsonify({"error": "Você precisa estar logado!"}), 401
    
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado!"}), 404
    
    #ATT OS DADOS DO USUARIO
    usuario.usuario = request.form['username']
    usuario.email = request.form['email']
    usuario.cargo = request.form['cargo']
    usuario.id_funcionario = request.form['funcionario']

    try:
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar usuário: {str(e)}"}), 500