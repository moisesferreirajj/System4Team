from flask import Blueprint, jsonify
from models import Pedido, Cliente, Produto, db

dados_painel_bp = Blueprint('dados_painel', __name__)

@dados_painel_bp.route("/dados_painel")
def dados_painel():
    # Buscar apenas pedidos finalizados (finalizado == True ou 1)
    pedidos_finalizados = Pedido.query.filter(Pedido.finalizado == True).all()
    total_vendas = 0
    total_pedidos = 0
    vendas_por_id = {}
    
    for pedido in pedidos_finalizados:
        if pedido.id_venda not in vendas_por_id:
            vendas_por_id[pedido.id_venda] = {'quantidade': 0, 'total_venda': 0}
            
        preco_total_pedido = pedido.produto.preco * pedido.quantidade
        vendas_por_id[pedido.id_venda]['quantidade'] += pedido.quantidade
        vendas_por_id[pedido.id_venda]['total_venda'] += preco_total_pedido
    
    for venda in vendas_por_id.values():
        total_vendas += venda['total_venda']
        total_pedidos += venda['quantidade']
    
    total_clientes = Cliente.query.count()

    # Dados a serem retornados na resposta JSON
    dados = {
        "vendas": total_vendas,
        "pedidos": total_pedidos,
        "clientes": total_clientes,
        "receita": total_vendas,
        "vendas_mensais": [200, 300, 250, 400, 350, 500],
        "despesas_mensais": [150, 200, 100, 250, 200, 300],
    }
    
    return jsonify(dados)
