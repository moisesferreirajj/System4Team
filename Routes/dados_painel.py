from flask import Blueprint, jsonify
from models import Pedido, Cliente, db

dados_painel_bp = Blueprint('dados_painel', __name__)

meses_portugues = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

@dados_painel_bp.route("/json/dados_painel")
def dados_painel():
    # Buscar apenas pedidos finalizados (finalizado == True ou 1)
    pedidos_finalizados = Pedido.query.filter(Pedido.finalizado == True).all()
    pedidos_nao_finalizados = Pedido.query.filter(Pedido.finalizado == False).all()

    total_vendas = 0
    total_nao_finalizadas = 0
    total_pedidos = 0  # Todos os pedidos, finalizados ou não
    vendas_por_id = {}
    vendas_por_mes = {}
    vendas_nao_finalizadas_por_mes = {}

    for pedido in pedidos_finalizados:
        if pedido.id_venda not in vendas_por_id:
            vendas_por_id[pedido.id_venda] = {'quantidade': 0, 'total_venda': 0}

        preco_total_pedido = pedido.produto.preco * pedido.quantidade
        vendas_por_id[pedido.id_venda]['quantidade'] += pedido.quantidade
        vendas_por_id[pedido.id_venda]['total_venda'] += preco_total_pedido

        mes = pedido.data_pedido.strftime('%Y-%m')
        if mes not in vendas_por_mes:
            vendas_por_mes[mes] = 0
        vendas_por_mes[mes] += preco_total_pedido

    # VENDAS NAO FINALIZADAS, DIFERENTE DO ACIMA
    for pedido in pedidos_nao_finalizados:
        preco_total_pedido = pedido.produto.preco * pedido.quantidade

        mes = pedido.data_pedido.strftime('%Y-%m')
        if mes not in vendas_nao_finalizadas_por_mes:
            vendas_nao_finalizadas_por_mes[mes] = 0
        vendas_nao_finalizadas_por_mes[mes] += preco_total_pedido

        # ACUMULANDO TODAS VENDAS, FINALIZADAS OU NAO FINALIZADAS
        total_nao_finalizadas += preco_total_pedido

        # Acumulando todos os pedidos, finalizados ou não
        total_pedidos += pedido.quantidade

    # TOTAL DE VENDAS E PEDIDOS ;P
    for venda in vendas_por_id.values():
        total_vendas += venda['total_venda']

    total_clientes = Cliente.query.count()

    # ARRAY DE MESES, PARA IDENTIFICAR COM O VALOR DE CADA UM
    vendas_mensais_array = [
        {"mes": meses_portugues[int(mes.split('-')[1]) - 1], "total": total}
        for mes, total in sorted(vendas_por_mes.items())
    ]

    vendas_nao_finalizadas_array = [
        {"mes": meses_portugues[int(mes.split('-')[1]) - 1], "total": total}
        for mes, total in sorted(vendas_nao_finalizadas_por_mes.items())
    ]

    # Dados a serem retornados na resposta JSON
    dados = {
        "vendas": total_vendas,
        "pedidos": total_pedidos,
        "clientes": total_clientes,
        "receita": total_nao_finalizadas,
        "vendas_mensais": vendas_mensais_array,
        "vendas_nao_finalizadas": vendas_nao_finalizadas_array,
    }

    return jsonify(dados)
