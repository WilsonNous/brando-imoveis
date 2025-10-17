import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    tipo = db.Column(db.String(50))
    valor = db.Column(db.Float)
    bairro = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    status = db.Column(db.String(20), default='ativo')

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'))
    data = db.Column(db.DateTime)

class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'), nullable=True)
    tipo_servico = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    data_solicitacao = db.Column(db.DateTime, default=datetime.now)
    data_agendamento = db.Column(db.DateTime, nullable=True)
    responsavel = db.Column(db.String(100))
    custo = db.Column(db.Numeric(10, 2))
    materiais = db.Column(db.Text)
    status = db.Column(db.Enum('pendente', 'andamento', 'concluido'), default='pendente')
