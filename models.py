from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ============================================================
#  IMÓVEL
# ============================================================
class Imovel(db.Model):
    __tablename__ = 'imovel'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    bairro = db.Column(db.String(100))
    descricao = db.Column(db.Text)

    # Legado – mantém compatibilidade com a antiga imagem salva em arquivo
    imagem = db.Column(db.String(255))

    status = db.Column(db.String(20), default='ativo')

    # Relações
    leads = db.relationship('Lead', backref='imovel', lazy=True)
    servicos = db.relationship('Servico', backref='imovel', lazy=True)

    fotos = db.relationship(
        'ImovelFoto',
        backref='imovel',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # ============================================================
    #  CAPA DO IMÓVEL
    # ============================================================
    @property
    def capa_url(self):
        """
        Retorna uma URL válida para exibição da capa:
        - Se houver foto marcada como capa → /foto/<id>
        - Se houver fotos mas nenhuma capa marcada → primeira foto
        - Se existir 'imagem' legado (antigo) → usa ela
        - Caso contrário → placeholder
        """
        if self.fotos:
            capa = next((f for f in self.fotos if f.is_capa), None)
            if capa:
                return f"/foto/{capa.id}"
            return f"/foto/{self.fotos[0].id}"

        if self.imagem:
            return self.imagem

        return "https://picsum.photos/800/600?blur=1"

    def __repr__(self):
        return f"<Imovel {self.codigo} - {self.tipo} ({self.bairro})>"


# ============================================================
#  LEAD
# ============================================================
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


# ============================================================
#  SERVIÇO
# ============================================================
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


# ============================================================
#  FOTOS DO IMÓVEL (BLOB)
# ============================================================
class ImovelFoto(db.Model):
    __tablename__ = 'imovel_fotos'

    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imovel.id'), nullable=False)

    # Conteúdo da imagem
    conteudo = db.Column(db.LargeBinary, nullable=False)

    # Tipo MIME (image/jpeg, image/png...)
    mimetype = db.Column(db.String(100), nullable=False, default="image/jpeg")

    # Indicador de capa
    is_capa = db.Column(db.Boolean, default=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ImovelFoto {self.id} -> Imovel {self.imovel_id}>"
