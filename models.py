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
