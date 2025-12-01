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

    # ⚠️ Mantemos campo antigo, mas agora não será usado como arquivo físico
    imagem = db.Column(db.String(255))

    status = db.Column(db.String(20), default='ativo')

    leads = db.relationship('Lead', backref='imovel', lazy=True)
    servicos = db.relationship('Servico', backref='imovel', lazy=True)

    fotos = db.relationship(
        'ImovelFoto',
        backref='imovel',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def capa(self):
        """Retorna a foto marcada como capa ou a primeira."""
        for f in self.fotos:
            if f.is_capa:
                return f
        return self.fotos[0] if self.fotos else None

    def __repr__(self):
        return f"<Imovel {self.codigo} - {self.tipo} ({self.bairro})>"


class Lead(db.Model):
    __tablename__ = 'lead'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    mensagem = db.Column(db.Text)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'))
    data = db.Column(db.DateTime, default=datetime.utcnow)


class Servico(db.Model):
    __tablename__ = 'servico'

    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'))
    tipo_servico = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_agendamento = db.Column(db.DateTime)
    responsavel = db.Column(db.String(100))
    custo = db.Column(db.Numeric(10, 2))
    materiais = db.Column(db.Text)
    status = db.Column(
        db.Enum('pendente', 'andamento', 'concluido', name='status_servico_enum'),
        default='pendente'
    )


class ImovelFoto(db.Model):
    __tablename__ = 'imovel_fotos'

    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'), nullable=False)

    # 📸 AGORA A IMAGEM É BLOB
    conteudo = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)

    # Se deve aparecer primeiro
    is_capa = db.Column(db.Boolean, default=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Foto {self.id}, capa={self.is_capa}>"
