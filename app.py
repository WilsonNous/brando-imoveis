from flask import Flask, render_template, request, redirect, jsonify, send_file
from datetime import datetime
from io import StringIO
import csv
import config
from models import db, Imovel, Lead, Servico
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

# ============================================================
# FILTRO DE FORMATAÇÃO MONETÁRIA (pt-BR)
# ============================================================
@app.template_filter('brl')
def format_brl(value):
    """Formata número no padrão monetário brasileiro."""
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
    """Verifica se o arquivo tem extensão permitida"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================================
# LOGGING ESTRUTURADO
# ============================================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
app.logger.info("🚀 Brando Imóveis iniciado com pool seguro de conexão MySQL.")

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
        return "Erro ao conectar ao banco de dados.", 500


@app.route('/imovel/<int:id>')
def imovel_detalhe(id):
    imovel = Imovel.query.get(id)
    if not imovel:
        return "Imóvel não encontrado.", 404
    return render_template('imovel.html', imovel=imovel)

# ============================================================
# LEADS E CONTATOS
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


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'GET':
        return render_template('contato.html')
    try:
        nome = request.form['nome']
        telefone = request.form['telefone']
        mensagem = request.form.get('mensagem', '')
        novo_lead = Lead(nome=nome, telefone=telefone, mensagem=mensagem, data=datetime.now())
        db.session.add(novo_lead)
        db.session.commit()
        return redirect("https://wa.me/5548991054216?text=Olá!%20Quero%20mais%20informações%20sobre%20os%20imóveis.")
    except Exception as e:
        app.logger.error(f"❌ Erro ao enviar contato: {e}")
        return "Erro ao enviar contato.", 500

# ============================================================
# BRANDINHO (IA básica)
# ============================================================
from brandinho_brain import responder

@app.route('/api/brandinho', methods=['POST'])
def brandinho():
    data = request.get_json(force=True) or {}
    q = (data.get('q') or '')
    try:
        answer = responder(q)
    except Exception as e:
        app.logger.error(f"❌ Erro no Brandinho: {e}")
        answer = "Tive um probleminha para processar agora 😅, tente novamente daqui a pouco."
    return jsonify({"answer": answer})

# ============================================================
# PAINEL ADMIN - IMÓVEIS
# ============================================================

@app.route('/admin')
def admin():
    q = request.args.get('q', '')
    base = Imovel.query
    if q:
        like = f"%{q}%"
        base = base.filter(
            (Imovel.codigo.ilike(like)) |
            (Imovel.tipo.ilike(like)) |
            (Imovel.bairro.ilike(like)) |
            (Imovel.descricao.ilike(like))
        )
    imoveis = base.order_by(Imovel.id.desc()).all()
    return render_template('admin.html', imoveis=imoveis, imovel=None)


@app.route('/admin/edit/<int:id>')
def admin_edit(id):
    imovel = Imovel.query.get(id)
    imoveis = Imovel.query.order_by(Imovel.id.desc()).all()
    return render_template('admin.html', imoveis=imoveis, imovel=imovel)


@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    item = Imovel.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/admin')

# ============================================================
# NOVA ROTA /admin/save COM UPLOAD DE IMAGEM
# ============================================================
@app.route('/admin/save', methods=['POST'])
def admin_save():
    form = request.form
    file = request.files.get('imagem_file')
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
        obj.valor = float(form.get('valor').replace(',', '.'))
    except:
        obj.valor = 0.0

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        obj.imagem = f"/static/uploads/{filename}"
        app.logger.info(f"📸 Imagem salva: {obj.imagem}")
    else:
        if not obj.imagem:
            obj.imagem = form.get('imagem')

    db.session.commit()
    app.logger.info(f"✅ Imóvel salvo: {obj.codigo}")
    return redirect('/admin')

# ============================================================
# EXPORTAÇÃO E IMPORTAÇÃO CSV
# ============================================================

@app.route('/admin/export')
def admin_export():
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id', 'codigo', 'tipo', 'valor (BRL)', 'bairro', 'descricao', 'imagem', 'status'])
    for i in Imovel.query.order_by(Imovel.id).all():
        valor_formatado = format_brl(i.valor)
        writer.writerow([
            i.id, i.codigo, i.tipo, valor_formatado, i.bairro,
            (i.descricao or '').replace('\n', ' '), i.imagem, i.status
        ])
    output = si.getvalue().encode('utf-8')
    return send_file(io.BytesIO(output), mimetype='text/csv', as_attachment=True, download_name='imoveis.csv')

@app.route('/admin/import', methods=['POST'])
def admin_import():
    file = request.files.get('csvfile')
    if not file:
        return redirect('/admin')
    stream = io.StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    count = 0
    for row in reader:
        codigo = row.get('codigo')
        if not codigo:
            continue
        obj = Imovel.query.filter_by(codigo=codigo).first() or Imovel()
        if not obj.id:
            db.session.add(obj)
        obj.codigo = codigo
        obj.tipo = row.get('tipo')
        try:
            obj.valor = float(row.get('valor') or 0)
        except:
            obj.valor = 0
        obj.bairro = row.get('bairro')
        obj.descricao = row.get('descricao')
        obj.imagem = row.get('imagem')
        obj.status = row.get('status') or 'ativo'
        count += 1
    db.session.commit()
    app.logger.info(f"✅ Importados/atualizados: {count}")
    return redirect('/admin')

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
            app.logger.error(f"❌ Erro ao salvar serviço: {erro}")

    imoveis = Imovel.query.filter_by(status="ativo").order_by(Imovel.id.desc()).all()
    return render_template("servicos.html", sucesso=sucesso, erro=erro, imoveis=imoveis)


@app.route('/admin/servicos')
def admin_servicos():
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
    s = Servico.query.get(id)
    if not s:
        return redirect('/admin/servicos')

    s.status = request.form.get('status', s.status)
    data_ag = request.form.get('data_agendamento')
    if data_ag:
        s.data_agendamento = datetime.strptime(data_ag, "%Y-%m-%d")
    s.responsavel = request.form.get('responsavel')
    s.materiais = request.form.get('materiais')

    # 💰 Aceita tanto vírgula quanto ponto
    custo = request.form.get('custo', '0').replace(',', '.')
    try:
        s.custo = float(custo)
    except ValueError:
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
