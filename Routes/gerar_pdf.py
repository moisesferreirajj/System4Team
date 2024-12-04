from flask import Blueprint, render_template, request, session, redirect, url_for, flash, make_response
from models import Pedido, Usuario, Cliente, Produto
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

gerar_relatorios_bp = Blueprint('gerar_relatorios', __name__)

# FONTE ARIAL
pdfmetrics.registerFont(TTFont('Arial', 'static/fonts/arial.ttf'))

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

    # VARIÁVEIS BÁSICAS
    total_vendas = 0
    total_receita = 0
    total_pedidos = 0
    total_pedidos_finalizados = 0
    vendas_por_id = {}

    for pedido in pedidos:
        preco_total_pedido = pedido.produto.preco * pedido.quantidade
        # CONTABILIZAR TODOS PEDIDOS
        total_receita += preco_total_pedido
        # CONTABILIZAR PEDIDOS FINALIZADOS E NÃO FINALIZADOS
        total_pedidos += 1
        if pedido.finalizado:
            total_vendas += preco_total_pedido
            total_pedidos_finalizados += 1

        # CONTABILIZAR VENDAS POR ID
        if pedido.id_venda not in vendas_por_id:
            vendas_por_id[pedido.id_venda] = {'quantidade': 0, 'total_venda': 0}
        
        vendas_por_id[pedido.id_venda]['quantidade'] += pedido.quantidade
        vendas_por_id[pedido.id_venda]['total_venda'] += preco_total_pedido

    total_clientes = Cliente.query.count()

    # GERANDO O PDF COM A BIBLIOTECA REPORTLAB
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # TITULO PDF
    c.setTitle("Relatório de Vendas - System4Team")
    logo_path = "http://127.0.0.1:5001/static/images/logo.png"
    c.drawImage(logo_path, 30, height - 50, width=80, height=25, mask='auto')  # LOGO E FUNDO
    c.setFont("Helvetica-Bold", 24)
    c.drawString(140, height - 50, "Relatório de Vendas - System4Team")
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(30, height - 80, width - 30, height - 80)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 130, "Resumo do Relatório:")
    
    # INFORMAÇÕES ANTES DA TABELA
    c.setFont("Arial", 14)
    c.drawString(30, height - 200, f"Total de Receita: R$ {total_receita:.2f} (todos os pedidos)")
    c.drawString(30, height - 170, f"Total de Vendas: R$ {total_vendas:.2f} (somente pedidos finalizados)")
    c.drawString(30, height - 290, f"Total de Clientes: {total_clientes}")
    c.drawString(30, height - 230, f"Total de Pedidos: {total_pedidos}")
    c.drawString(30, height - 260, f"Total de Pedidos Finalizados: {total_pedidos_finalizados}")
    
    # ADICIONANDO BORDAS AS TABELAS
    y_position = height - 340
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y_position, "ID Pedido")
    c.drawString(150, y_position, "Cliente")
    c.drawString(270, y_position, "Produto")
    c.drawString(390, y_position, "Quantidade")
    c.drawString(510, y_position, "Preço Total")
    c.setLineWidth(0.5)
    c.line(30, y_position - 5, 600, y_position - 5)
    y_position -= 20
    c.setFont("Arial", 14)

    # PEDIDOS INFORMAÇÕES
    for pedido in pedidos:
        # ID DO PEDIDO CENTRALIZADO
        c.drawString(30, y_position, str(pedido.id_venda))
        status = "F" if pedido.finalizado else "N"
        status_color = colors.green if pedido.finalizado else colors.red
        c.setFillColor(status_color)
        c.circle(70, y_position + 3, 7, fill=1)  # CÍRCULO FERRADO
        c.setFillColor(colors.white)
        c.setFont("Arial", 12)
        c.drawString(66, y_position - 2, status)  # TEXTO DENTRO DO CÍRCULO
        c.setFillColor(colors.black)  # RETORNA A COR NORMAL
        # INFORMAÇÕES ADICIONAIS CENTRALIZADAS
        c.drawString(150, y_position, pedido.cliente.nome)
        c.drawString(270, y_position, pedido.produto.nome)
        c.drawString(390, y_position, str(pedido.quantidade))
        c.drawString(510, y_position, f"R$ {pedido.produto.preco * pedido.quantidade:.2f}")        
        y_position -= 30
    
    # TABELA SEPARADA, APENAS ID PEDIDO E DATA VENDA
    y_position -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y_position, "ID Pedido")
    c.drawString(520, y_position, "Data")
    c.setLineWidth(0.5)
    c.line(30, y_position - 5, 600, y_position - 5)
    y_position -= 20
    c.setFont("Arial", 14)

    for pedido in pedidos:
        c.drawString(30, y_position, str(pedido.id_venda))
        status = "F" if pedido.finalizado else "N"
        status_color = colors.green if pedido.finalizado else colors.red
        c.setFillColor(status_color)
        c.circle(70, y_position + 3, 7, fill=1)  # CÍRCULO PEQUENO
        c.setFillColor(colors.white)
        c.setFont("Arial", 12)
        c.drawString(66, y_position - 2, status)  # N OU F NO CÍRCULO
        c.setFillColor(colors.black)  # RETORNA COR PRETA
        c.drawString(520, y_position, pedido.data_pedido.strftime('%d/%m/%Y'))
        y_position -= 30

    # FINALIZANDO E SALVANDO O PDF
    c.save()

    # ENVIAR O PDF GERADO COMO RESPOSTA
    pdf = buffer.getvalue()
    buffer.close()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="Relatório de Vendas - System4Team.pdf"'
    return response
