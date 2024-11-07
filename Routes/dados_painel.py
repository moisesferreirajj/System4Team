from flask import Blueprint, jsonify
from models import Pedido, Cliente, db

dados_painel_bp = Blueprint('dados_painel', __name__)

@dados_painel_bp.route("/dados_painel")
def dados_painel():
    # BUSCAR DADOS AKI
    total_vendas = 0
    total_pedidos = 0
    pedidos = Pedido.query.all()

    for pedido in pedidos:
        total_vendas += pedido.preco_total
        total_pedidos += pedido.quantidade
        
    #QUANTIDADE DE CLIENTES
    total_clientes = Cliente.query.count()

    dados = {
        "vendas": total_vendas,
        "pedidos": total_pedidos,
        "clientes": total_clientes,
        "receita": total_vendas,
        "vendas_mensais": [200, 300, 250, 400, 350, 500],
        "despesas_mensais": [150, 200, 100, 250, 200, 300],
    }
    return jsonify(dados)
