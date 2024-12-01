from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from models import Usuario, Pedido, Produto, Empresa, Cliente, Cargo, db 
from sqlalchemy import func, extract, cast, Date
from datetime import datetime, timedelta

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

    # Calcular as vendas anuais e mensais
    hoje = datetime.now()
    um_ano_atras = hoje - timedelta(days=365)
    um_mes_atras = hoje - timedelta(days=30)
    uma_semana_atras = hoje - timedelta(days=7)

    vendas_anuais = db.session.query(
        func.sum(Produto.preco * Pedido.quantidade).label('total')
    ).join(Pedido, Produto.id == Pedido.id_produto
    ).filter(Pedido.finalizado == True, Pedido.data_pedido >= um_ano_atras).scalar() or 0

    vendas_mensais = db.session.query(
        func.sum(Produto.preco * Pedido.quantidade).label('total')
    ).join(Pedido, Produto.id == Pedido.id_produto
    ).filter(Pedido.finalizado == True, Pedido.data_pedido >= um_mes_atras).scalar() or 0

    vendas_semanais = db.session.query(
        func.sum(Produto.preco * Pedido.quantidade).label('total')
    ).join(Pedido, Produto.id == Pedido.id_produto
    ).filter(Pedido.finalizado == True, Pedido.data_pedido >= uma_semana_atras).scalar() or 0

    #FORMATAÇÃO
    vendas_anuais_formatado = f'{vendas_anuais:,.2f}'.replace(",", ".")
    vendas_mensais_formatado = f'{vendas_mensais:,.2f}'.replace(",", ".") if vendas_mensais else '0'
    vendas_semanais_formatado = f'{vendas_semanais:,.2f}'.replace(",", ".") if vendas_mensais else '0'

    return render_template(
        'vendas.html',
        username=username,
        imagem_usuario=imagem_usuario,
        cargo=cargo_relacionado.nome,
        vendas_anuais=vendas_anuais_formatado,
        vendas_mensais=vendas_mensais_formatado,
        vendas_semanais=vendas_semanais_formatado
    )
    
@vendas_bp.route("/json/dados-vendas")
def dados():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('auth.login'))
    
    username = session['username']
    if username and username[0].islower():
        username = username.capitalize()

    usuario = Usuario.query.filter_by(usuario=username).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('auth.login'))

    cargo_relacionado = usuario.cargo_relacionado
    if not cargo_relacionado or cargo_relacionado.id not in [1, 2, 3, 4, 5]:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))

    hoje = datetime.now()
    um_ano_atras = hoje - timedelta(days=365)

    # Consultar os produtos mais vendidos no último ano
    produtos_mais_vendidos = db.session.query(
        Produto.nome,
        func.sum(Pedido.quantidade).label('quantidade_vendida'),
        func.sum(Produto.preco * Pedido.quantidade).label('lucro')
    ).join(Pedido, Produto.id == Pedido.id_produto
    ).filter(Pedido.finalizado == True, Pedido.data_pedido >= um_ano_atras).group_by(Produto.id).order_by(func.sum(Pedido.quantidade).desc()).limit(5).all()

    # Organizar os dados dos produtos mais vendidos
    produtos_dados = []
    labels = []
    vendas_produtos = []
    for produto in produtos_mais_vendidos:
        produtos_dados.append({
            'nome': produto.nome,
            'quantidade': produto.quantidade_vendida,
            'lucro': produto.lucro
        })
        labels.append(produto.nome)  # Labels como nomes dos produtos
        vendas_produtos.append(produto.lucro)  # Lucro de cada produto

    # Retornar os dados em formato JSON
    return jsonify({
        'produtos_mais_vendidos': produtos_dados,
        'labels': labels,
        'vendas_produtos': vendas_produtos
    })

@vendas_bp.route("/json/listagem-pedidos")
def listagem():
    if 'username' not in session:
        flash('Você precisa fazer login primeiro!')
        return redirect(url_for('auth.login'))
    
    username = session['username']
    if username and username[0].islower():
        username = username.capitalize()

    usuario = Usuario.query.filter_by(usuario=username).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('auth.login'))

    cargo_relacionado = usuario.cargo_relacionado
    if not cargo_relacionado or cargo_relacionado.id not in [1, 2, 3, 4, 5]:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))

    # Obter todos os pedidos com os produtos e quantidades
    pedidos = db.session.query(
        Pedido.id_venda,
        Pedido.id_cliente,
        Pedido.id_empresa,
        Pedido.data_pedido,
        Pedido.finalizado,
        Cliente.nome.label('cliente_nome'),
        Empresa.nome.label('empresa_nome'),
        Produto.nome.label('produto_nome'),
        Pedido.quantidade.label('quantidade')
    ).join(Cliente, Pedido.id_cliente == Cliente.id).join(Empresa, Pedido.id_empresa == Empresa.id).join(Produto, Pedido.id_produto == Produto.id).all()

    pedidos_serializados = []
    for pedido in pedidos:
        pedidos_serializados.append({
            'id_venda': pedido.id_venda,
            'id_cliente': pedido.id_cliente,
            'cliente_nome': pedido.cliente_nome,
            'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
            'id_empresa': pedido.id_empresa,
            'empresa_nome': pedido.empresa_nome,
            'produto_nome': pedido.produto_nome,
            'quantidade': pedido.quantidade,
            'finalizado': pedido.finalizado
        })

    return jsonify({
        'pedidos': pedidos_serializados
    })
