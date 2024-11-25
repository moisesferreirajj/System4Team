from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100))

    def __repr__(self):
        return f'<Empresa {self.nome}>'

class Cargo(db.Model):
    __tablename__ = 'cargos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Cargo {self.nome}>'

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(15))
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'))

    cargo_relacionado = db.relationship('Cargo', backref='funcionarios')
    empresa_relacionada = db.relationship('Empresa', backref='funcionarios')

    def __repr__(self):
        return f'<Funcionário {self.nome}>'

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'))

    empresa_relacionada = db.relationship('Empresa', backref='clientes')

    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'))

    empresa_relacionada = db.relationship('Empresa', backref='produtos')

    def __repr__(self):
        return f'<Produto {self.nome}>'

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    quantidade = db.Column(db.Integer, nullable=False)
    id_venda = db.Column(db.Integer, nullable=False)
    data_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    finalizado = db.Column(db.Boolean, nullable=False, default=False)
    cliente = db.relationship('Cliente', backref='pedidos')
    produto = db.relationship('Produto', backref='pedidos')
    funcionario = db.relationship('Funcionario', backref='pedidos')
    empresa = db.relationship('Empresa', backref='pedidos')

    def __repr__(self):
        return f'<Pedido {self.id}, Cliente {self.id_cliente}, Produto {self.id_produto}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'))
    imagem = db.Column(db.String(255))  # URL ou caminho da imagem
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))

    cargo_relacionado = db.relationship('Cargo', backref='usuarios')
    funcionario_relacionado = db.relationship('Funcionario', backref='usuarios')

    def __repr__(self):
        return f'<CodigoRecuperacao {self.codigo} para {self.email}>'
    
    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f'<Usuário {self.usuario}>'
    
class CodigoRecuperacao(db.Model):
    __tablename__ = 'codigos_recuperacao'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usado = db.Column(db.Boolean, default=True)
    usuario = db.relationship('Usuario', backref='codigos_recuperacao')

class Despesa(db.Model):
    __tablename__ = 'despesas'
    
    id = db.Column(db.Integer, primary_key=True)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_despesa = db.Column(db.DateTime, nullable=False)
    
    empresa_relacionada = db.relationship('Empresa', backref='despesas')
    
    def __repr__(self):
        return f'<Despesa {self.id}, Valor {self.valor}, Data {self.data_despesa}>'
