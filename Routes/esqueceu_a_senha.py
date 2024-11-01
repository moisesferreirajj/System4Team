from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_mail import Mail, Message
from models import Usuario, CodigoRecuperacao, db
import random
import string
import bcrypt
import re

mail = Mail()  #INICIALIZA O SERVIÇO DE EMAIL AQUI TAMBEM
esqueceu_a_senha_bp = Blueprint('esqueceu_a_senha', __name__)

def init_mail(app):
    mail.init_app(app)

@esqueceu_a_senha_bp.route("/esqueceu-a-senha", methods=['GET', 'POST'])
def esqueceu():
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            codigo_recuperacao = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            codigo = CodigoRecuperacao(email=email, codigo=codigo_recuperacao, usuario_id=usuario.id, usado=True)
            db.session.add(codigo)
            db.session.commit()

            # URL da logo
            logo_url = "https://cdn.discordapp.com/attachments/1273695375991115856/1302001573785768088/logo.png?ex=672686f5&is=67253575&hm=741949539d1b580b1591e76d30d55d8d1433966973e06ce7e036626ff992fcc9&"
            msg = Message('Recuperação de Senha', recipients=[email])
        #     if usuario and usuario.funcionario_relacionado:
        #      nome_usuario = usuario.funcionario_relacionado.nome
        # else:
        #      nome_usuario = usuario.usuario  # Caso não tenha um funcionário relacionado, usa o identificador
        msg.html = f'''
<html>
    <body>
        <h1 style="text-align: center; color: #4A90E2;">Recuperação de Senha - System4Team</h1>
        <div style="text-align: center;">
            <img src="{logo_url}" alt="Logo System4Team" style="width: 200px; height: auto;">
        </div>
        <p style="font-size: 16px; text-align: center;">
            Olá! Aqui é da System4Team! Seu código de recuperação é: <strong style="font-size: 24px; color: #D0021B;">{codigo_recuperacao}</strong>
        </p>
        <p style="text-align: center;">
            Caso não tenha solicitado esta recuperação, ignore este e-mail.
        </p>
        <p style="text-align: center; color: #999;">A equipe System4Team</p>
    </body>
</html>
            '''
        mail.send(msg)
        flash('Código de recuperação enviado para seu e-mail!', 'success')
        session['email'] = email
        return redirect(url_for('esqueceu_a_senha.confirma_codigo'))
    else:
        flash('E-mail não encontrado!', 'danger')

    return render_template('esqueceu-a-senha.html')

@esqueceu_a_senha_bp.route("/confirma-codigo", methods=['GET', 'POST'])
def confirma_codigo():
    if request.method == 'POST':
        codigo_inserido = request.form.get('codigo')
        email = session.get('email')

        if not email:
            flash('Nenhum e-mail encontrado na sessão.', 'danger')
            return redirect(url_for('esqueceu_a_senha.esqueceu'))

        codigo = CodigoRecuperacao.query.filter_by(email=email, codigo=codigo_inserido, usado=True).first()
        if codigo:
            flash('Código confirmado! Você pode redefinir sua senha.', 'success')

            codigo.usado = False
            db.session.commit() 

            session['codigo_confirmado'] = True
            return redirect(url_for('esqueceu_a_senha.alterar_senha'))
        else:
            flash('Código incorreto ou já utilizado. Tente novamente.', 'danger')

    return render_template('confirma_codigo.html')

@esqueceu_a_senha_bp.route("/alterar-senha", methods=['GET', 'POST'])
def alterar_senha():
    if not session.get('codigo_confirmado'):
        flash('Você deve confirmar o código de recuperação antes de alterar a senha.', 'danger')
        return redirect(url_for('esqueceu_a_senha.esqueceu'))

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        password_pattern = r'^(?=.*[A-Z])(?=(.*[0-9]){1})(?=.*[!@#$%^&*()_+\[\]{};":\\|,.<>?]).{6,}$'
        if not re.match(password_pattern, nova_senha):
            flash("A senha deve conter pelo menos 1 letra maiúscula, 1 número e 1 símbolo especial.", "danger")
            return redirect(url_for('esqueceu_a_senha.alterar_senha'))

        if nova_senha != confirmar_senha:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for('esqueceu_a_senha.alterar_senha'))

        email = session.get('email')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            hashed_password = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            usuario.senha = hashed_password  #ATRIBUI O DEMONIO DO BCRYPT NA SENHA
            db.session.commit()  #ALTERA AS INFORMACOES DO USUARIO
            flash('Senha redefinida com sucesso!', 'success')
            session.pop('codigo_confirmado', None)
            return redirect(url_for('auth.login'))  #REDIRECIONA PARA O LOGIN
        else:
            flash('Erro ao redefinir a senha.', 'danger')

    return render_template('alterar-senha.html')
