from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Imovel(db.Model):
    __tablename__ = 'imovel'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    bairro = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    status = db.Column(db.String(20), default='ativo')

    leads = db.relationship('Lead', backref='imovel', lazy=True)
    servicos = db.relationship('Servico', backref='imovel', lazy=True)

    def __repr__(self):
        return f"<Imovel {self.codigo} - {self.tipo} ({self.bairro})>"


class Lead(db.Model):
    __tablename__ = 'lead'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    mensagem = db.Column(db.Text)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Lead {self.nome} - {self.telefone}>"


class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'), nullable=True)
    tipo_servico = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_agendamento = db.Column(db.DateTime, nullable=True)
    responsavel = db.Column(db.String(100))
    custo = db.Column(db.Numeric(10, 2))
    materiais = db.Column(db.Text)
    status = db.Column(
        db.Enum('pendente', 'andamento', 'concluido', name='status_servico_enum'),
        default='pendente'
    )

    def __repr__(self):
        return f"<Servico {self.tipo_servico or ''} - {self.nome_cliente}>"
