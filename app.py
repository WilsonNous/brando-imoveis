from flask import Flask, render_template, request, redirect, jsonify, send_file, session
from datetime import datetime
from io import StringIO
import csv
import config
from models import db, Imovel, Lead, Servico, ImovelFoto
import io
import logging
from sqlalchemy.pool import QueuePool
import os
from werkzeug.utils import secure_filename

# ============================================================
# INICIALIZAÇÃO FLASK + BANCO
# ============================================================

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = config.SECRET_KEY

ADMIN_PASSWORD = "brando2025"  # 🔐 Senha de acesso ao painel


# ============================================================
# LOGIN DO ADMIN
# ============================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == ADMIN_PASSWORD:
            session["admin_auth"] = True
            return redirect("/admin")
        return render_template("admin_login.html", erro="Senha incorreta.")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_auth", None)
    return redirect("/admin/login")


def require_admin():
    """Bloqueia acesso ao painel se não estiver logado."""
    if not session.get("admin_auth"):
        return redirect("/admin/login")


# ============================================================
# FILTRO DE FORMATAÇÃO MONETÁRIA (pt-BR)
# ============================================================

@app.template_filter('brl')
def format_brl(value):
    try:
        value = float(value)
        return f"R$ {value:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"


# 🔧 Engine Options (mantém conexão estável com MySQL HostGator)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 5,
    "max_overflow": 10,
    "poolclass": QueuePool,
    "connect_args": {"connect_timeout": 10},
}

db.init_app(app)


# ============================================================
# CONFIGURAÇÃO DE UPLOAD DE IMAGENS
# ============================================================

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
app.logger.info("🚀 Brando Imóveis iniciado com pool seguro.")


# ============================================================
# PÁGINAS PÚBLICAS
# ============================================================

@app.route('/')
def home():
    try:
        imoveis = Imovel.query.filter_by(status='ativo').all()
        return render_template('index.html', imoveis=imoveis)
    except Exception as e:
        app.logger.error(f"❌ Erro ao consultar imóveis: {e}")
        return "Erro ao conectar ao banco.", 500


@app.route('/imovel/<int:id>')
def imovel_detalhe(id):
    imovel = Imovel.query.get(id)
    if not imovel:
        return "Imóvel não encontrado.", 404

    fotos = []
    if imovel.imagem:
        fotos.append(imovel.imagem)
    for f in imovel.fotos:
        fotos.append(f.caminho)

    if not fotos:
        fotos = ["https://picsum.photos/800/600?blur=1"]

    return render_template("imovel.html", imovel=imovel, fotos=fotos)


# ============================================================
# DEFINIR CAPA
# ============================================================

@app.route("/admin/imovel/<int:imovel_id>/set_capa/<int:foto_id>", methods=["POST"])
def set_capa(imovel_id, foto_id):
    r = require_admin()
    if r: return r

    imovel = Imovel.query.get_or_404(imovel_id)
    foto = ImovelFoto.query.get_or_404(foto_id)

    imovel.imagem = foto.caminho
    db.session.commit()

    return redirect(f"/admin/edit/{imovel_id}")


# ============================================================
# LEADS
# ============================================================

@app.route('/lead', methods=['POST'])
def lead():
    try:
        nome = request.form['nome']
        telefone = request.form['telefone']
        mensagem = request.form.get('mensagem', '')
        imovel_id = request.form.get('imovel_id')

        novo_lead = Lead(
            nome=nome,
            telefone=telefone,
            mensagem=mensagem,
            imovel_id=imovel_id,
            data=datetime.now()
        )
        db.session.add(novo_lead)
        db.session.commit()

        msg = f"Olá! Tenho interesse no imóvel código {imovel_id}" if imovel_id else "Olá! Tenho interesse em imóveis da Brando."
        return redirect(f"https://wa.me/5548991054216?text={msg}")

    except Exception as e:
        app.logger.error(f"❌ Erro ao registrar lead: {e}")
        return "Erro ao enviar lead.", 500


# ============================================================
# PAINEL ADMIN — LISTA / EDITAR / SALVAR
# ============================================================

@app.route('/admin')
def admin():
    r = require_admin()
    if r: return r

    q = request.args.get('q', '')
    base = Imovel.query
    if q:
        like = f"%{q}%"
        base = base.filter(
            Imovel.codigo.ilike(like) |
            Imovel.tipo.ilike(like) |
            Imovel.bairro.ilike(like) |
            Imovel.descricao.ilike(like)
        )

    imoveis = base.order_by(Imovel.id.desc()).all()
    return render_template('admin.html', imoveis=imoveis, imovel=None)


@app.route('/admin/edit/<int:id>')
def admin_edit(id):
    r = require_admin()
    if r: return r

    imovel = Imovel.query.get(id)
    imoveis = Imovel.query.order_by(Imovel.id.desc()).all()
    return render_template('admin.html', imoveis=imoveis, imovel=imovel)


@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    r = require_admin()
    if r: return r

    item = Imovel.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/admin')


# ============================================================
# SALVAR IMÓVEL + UPLOAD MULTIPLO
# ============================================================

@app.route('/admin/save', methods=['POST'])
def admin_save():
    r = require_admin()
    if r: return r

    form = request.form
    iid = form.get('id')

    obj = Imovel.query.get(int(iid)) if iid else Imovel()
    if not iid:
        db.session.add(obj)

    obj.codigo = form.get('codigo')
    obj.tipo = form.get('tipo')
    obj.bairro = form.get('bairro')
    obj.descricao = form.get('descricao')
    obj.status = form.get('status', 'ativo')

    try:
        obj.valor = float((form.get('valor') or "0").replace(',', '.'))
    except:
        obj.valor = 0.0

    # 🔥 Upload múltiplo
    files = request.files.getlist('imagens')
    for file in files:
        if file and allowed_file(file.filename):
            original = secure_filename(file.filename)
            unique_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{original}"

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            file.save(filepath)

            rel_path = f"/static/uploads/{unique_name}"

            foto = ImovelFoto(imovel=obj, caminho=rel_path)
            db.session.add(foto)

            if not obj.imagem:
                obj.imagem = rel_path

    if not obj.imagem:
        obj.imagem = form.get('imagem')

    db.session.commit()
    return redirect('/admin')


# ============================================================
# EXPORTAÇÃO / IMPORTAÇÃO CSV
# ============================================================

@app.route('/admin/export')
def admin_export():
    r = require_admin()
    if r: return r

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id', 'codigo', 'tipo', 'valor', 'bairro', 'descricao', 'imagem', 'status'])

    for i in Imovel.query.order_by(Imovel.id).all():
        writer.writerow([
            i.id, i.codigo, i.tipo, i.valor, i.bairro,
            (i.descricao or '').replace("\n", " "),
            i.imagem, i.status
        ])

    output = si.getvalue().encode('utf-8')
    return send_file(io.BytesIO(output), mimetype='text/csv',
                     as_attachment=True, download_name='imoveis.csv')


# ============================================================
# SERVIÇOS (PÚBLICO E ADMIN)
# ============================================================

@app.route("/servicos", methods=["GET", "POST"])
def servicos():
    sucesso, erro = False, None

    if request.method == "POST":
        try:
            nome = request.form.get("nome_cliente")
            telefone = request.form.get("telefone")
            imovel_id = request.form.get("imovel_id")
            tipo_servico = request.form.get("tipo_servico")
            descricao = request.form.get("descricao")

            imovel_id = int(imovel_id) if imovel_id and imovel_id.isdigit() else None

            novo = Servico(
                nome_cliente=nome,
                telefone=telefone,
                imovel_id=imovel_id,
                tipo_servico=tipo_servico,
                descricao=descricao,
                data_solicitacao=datetime.now(),
                status="pendente",
            )

            db.session.add(novo)
            db.session.commit()
            sucesso = True

        except Exception as e:
            db.session.rollback()
            erro = str(e)

    imoveis = Imovel.query.filter_by(status="ativo").order_by(Imovel.id.desc()).all()
    return render_template("servicos.html", sucesso=sucesso, erro=erro, imoveis=imoveis)


@app.route('/admin/servicos')
def admin_servicos():
    r = require_admin()
    if r: return r

    servicos = (
        db.session.query(Servico)
        .outerjoin(Imovel)
        .options(db.contains_eager(Servico.imovel))
        .order_by(Servico.data_solicitacao.desc())
        .all()
    )
    return render_template('admin_servicos.html', servicos=servicos)


@app.route('/admin/servicos/update/<int:id>', methods=['POST'])
def update_servico(id):
    r = require_admin()
    if r: return r

    s = Servico.query.get(id)
    if not s:
        return redirect('/admin/servicos')

    s.status = request.form.get('status', s.status)
    data_ag = request.form.get('data_agendamento')
    if data_ag:
        s.data_agendamento = datetime.strptime(data_ag, "%Y-%m-%d")
    s.responsavel = request.form.get('responsavel')
    s.materiais = request.form.get('materiais')

    custo = request.form.get('custo', '0').replace(',', '.')
    try:
        s.custo = float(custo)
    except:
        s.custo = 0.0

    db.session.commit()
    return redirect('/admin/servicos')


# ============================================================
# PÁGINA DE TEMPORADA
# ============================================================

@app.route('/temporada')
def temporada():
    imoveis = Imovel.query.filter(Imovel.status == 'ativo').all()
    return render_template('temporada.html', imoveis=imoveis)


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Banco de dados ok")
    app.run(debug=True)
