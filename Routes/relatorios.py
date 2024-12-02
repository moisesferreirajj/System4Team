from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import Pedido, Usuario, Cliente, Produto, db
from sqlalchemy import func

relatorios_bp = Blueprint('relatorios', __name__)

meses_portugues = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# RELATÓRIOS, COMEÇA A LÓGICA AQUI
@relatorios_bp.route("/relatorios", methods=['GET', 'POST'])
def relatorios():
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

    # OBTER VALORES DE MÊS E ANO
    mes = request.form.get('mes')
    ano = request.form.get('ano')

    # OBTER TODOS OS PEDIDOS
    pedidos = Pedido.query.all()  # Buscar todos os pedidos, sem filtrar por finalizado

    # CRIAR LISTA DE MESES E ANOS ÚNICOS
    meses_anos = []
    for pedido in pedidos:
        mes_ano = (pedido.data_pedido.month, pedido.data_pedido.year)
        if mes_ano not in meses_anos:  # Evitar duplicatas
            meses_anos.append(mes_ano)

    # FILTRA O PEDIDO DO MÊS E ANO
    if ano:
        pedidos = [pedido for pedido in pedidos if pedido.data_pedido.year == int(ano)]
    if mes:
        pedidos = [pedido for pedido in pedidos if pedido.data_pedido.month == int(mes)]

    # CALCULAR VENDAS E PEDIDOS POR ID_VENDA
    total_pedidos = 0
    venda_produto_quant = {} 

    for pedido in pedidos:
        if pedido.id_venda not in venda_produto_quant:
            venda_produto_quant[pedido.id_venda] = {
                'quantidade': 0, 
                'total_venda': 0,
                'produtos': []  # LISTA ARMAZENAR CADA PRODUTO
            }
    #CALCULAR PREÇO TOTAL DE PEDIDOS
    preco_total_pedido = pedido.produto.preco * pedido.quantidade
    venda_produto_quant[pedido.id_venda]['produtos'].append({
        'produto_nome': pedido.produto.nome,
        'quantidade': pedido.quantidade,
        'preco_total': preco_total_pedido
    })
    
    # Atualiza a quantidade total de produtos e o total de vendas por venda
    venda_produto_quant[pedido.id_venda]['quantidade'] += pedido.quantidade
    venda_produto_quant[pedido.id_venda]['total_venda'] += preco_total_pedido

    for pedido in pedidos:
        preco_total_pedido = pedido.produto.preco * pedido.quantidade
        pedido.preco_total = preco_total_pedido

    # Utilizar query pq eu já to morto - S2, Moises - 02/12
    total_clientes = Cliente.query.count()
    total_pedidos = Pedido.query.count()
    
    total_vendas = db.session.query(func.sum(Produto.preco * Pedido.quantidade).label('total')
    ).join(Pedido, Produto.id == Pedido.id_produto
    ).filter(Pedido.finalizado == True).scalar() or 0
    
    imagem_usuario = usuario.imagem if usuario.imagem else 'default.png'


    return render_template(
        'relatorios.html',
        username=username,
        imagem_usuario=imagem_usuario,
        cargo=cargo_nome,
        venda_produto_quant=venda_produto_quant,
        pedidos=pedidos,
        total_vendas=total_vendas,
        total_pedidos=total_pedidos,
        total_clientes=total_clientes,
        meses_anos=meses_anos,
        meses_portugues=meses_portugues
    )

