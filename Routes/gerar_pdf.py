from flask import Blueprint, render_template, request, session, redirect, url_for, flash, make_response
from models import Pedido, Usuario, Cliente, Produto, db
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

gerar_relatorios_bp = Blueprint('gerar_relatorios', __name__)

@gerar_relatorios_bp.route("/gerar-relatorio-pdf", methods=['POST'])
def gerar_relatorio_pdf():
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
    if not cargo_relacionado:
        session.pop('username', None)
        flash('Você não tem permissão para acessar o painel!')
        return redirect(url_for('auth.login'))

    mes = request.form.get('mes')
    ano = request.form.get('ano')

    pedidos = Pedido.query.all()

    if ano:
        pedidos = [pedido for pedido in pedidos if pedido.data_pedido.year == int(ano)]
    if mes:
        pedidos = [pedido for pedido in pedidos if pedido.data_pedido.month == int(mes)]

    total_vendas = 0
    total_pedidos = 0
    vendas_por_id = {}

    for pedido in pedidos:
        if pedido.id_venda not in vendas_por_id:
            vendas_por_id[pedido.id_venda] = {'quantidade': 0, 'total_venda': 0}
        
        preco_total_pedido = pedido.produto.preco * pedido.quantidade
        vendas_por_id[pedido.id_venda]['quantidade'] += pedido.quantidade
        vendas_por_id[pedido.id_venda]['total_venda'] += preco_total_pedido

    for venda in vendas_por_id.values():
        total_vendas += venda['total_venda']
        total_pedidos += venda['quantidade']

    total_clientes = Cliente.query.count()

    # Gerando o conteúdo do PDF com ReportLab
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Títulos
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 40, "Relatório de Vendas")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 80, f"Total de Vendas: R$ {total_vendas:.2f}")
    c.drawString(100, height - 100, f"Total de Pedidos: {total_pedidos}")
    c.drawString(100, height - 120, f"Total de Clientes: {total_clientes}")

    # Adicionar informações dos pedidos
    y_position = height - 160
    c.setFont("Helvetica", 10)
    for pedido in pedidos:
        c.drawString(100, y_position, f"Pedido ID: {pedido.id_venda}, Cliente: {pedido.cliente.nome}, Total: R$ {pedido.produto.preco * pedido.quantidade:.2f}")
        y_position -= 20
        if y_position < 100:  # Adicionar nova página se o espaço for pequeno
            c.showPage()
            y_position = height - 40

    c.showPage()
    c.save()

    # Enviar o PDF gerado como resposta
    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
    return response
