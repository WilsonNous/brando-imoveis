
from flask import Flask, render_template, request, redirect, jsonify, send_file
from datetime import datetime
from io import StringIO
import csv
import config
from models import db, Imovel, Lead, Servico
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = config.SECRET_KEY
db.init_app(app)

@app.route('/')
def home():
    try:
        imoveis = Imovel.query.filter_by(status='ativo').all()
        return render_template('index.html', imoveis=imoveis)
    except Exception as e:
        print("❌ Erro ao consultar imóveis:", e)
        return "Erro ao conectar ao banco de dados.", 500

@app.route('/imovel/<int:id>')
def imovel_detalhe(id):
    imovel = Imovel.query.get(id)
    if not imovel:
        return "Imóvel não encontrado.", 404
    return render_template('imovel.html', imovel=imovel)

@app.route('/lead', methods=['POST'])
def lead():
    try:
        nome = request.form['nome']
        telefone = request.form['telefone']
        mensagem = request.form.get('mensagem', '')
        imovel_id = request.form.get('imovel_id')
        novo_lead = Lead(
            nome=nome, telefone=telefone, mensagem=mensagem,
            imovel_id=imovel_id, data=datetime.now()
        )
        db.session.add(novo_lead)
        db.session.commit()
        msg = f"Olá! Tenho interesse no imóvel código {imovel_id}" if imovel_id else "Olá! Tenho interesse em imóveis da Brando."
        return redirect(f"https://wa.me/5548991054216?text={msg}")
    except Exception as e:
        print("❌ Erro ao registrar lead:", e)
        return "Erro ao enviar lead.", 500

@app.route('/contato', methods=['GET','POST'])
def contato():
    if request.method == 'GET':
        return render_template('contato.html')
    try:
        nome = request.form['nome']
        telefone = request.form['telefone']
        mensagem = request.form.get('mensagem','')
        novo_lead = Lead(nome=nome, telefone=telefone, mensagem=mensagem, imovel_id=None, data=datetime.now())
        db.session.add(novo_lead)
        db.session.commit()
        return redirect(f"https://wa.me/5548991054216?text=Olá!%20Quero%20mais%20informações%20sobre%20os%20imóveis.")
    except Exception as e:
        print("❌ Erro ao enviar contato:", e)
        return "Erro ao enviar contato.", 500

@app.route('/api/brandinho', methods=['POST'])
def brandinho():
    data = request.get_json(force=True) or {}
    q = (data.get('q') or '').lower()
    answer = "Posso te ajudar a encontrar casas e apartamentos. Diga um bairro ou faixa de preço!"
    if 'canas' in q:
        found = Imovel.query.filter(Imovel.bairro.ilike('%canas%')).all()
        if found:
            cards = ', '.join([f"{x.tipo} {x.codigo} (R$ {x.valor:,.0f})" for x in found])
            answer = f"Tenho estas opções em Canasvieiras: {cards}. Você pode ver mais na página inicial."
        else:
            answer = "No momento não encontrei imóveis em Canasvieiras. Quer tentar outro bairro?"
    elif 'apart' in q or 'apto' in q:
        found = Imovel.query.filter(Imovel.tipo.ilike('%apart%')).all()
        if found:
            answer = f"Encontrei {len(found)} apartamentos. Use a busca na página ou diga um bairro."
    elif 'casa' in q:
        found = Imovel.query.filter(Imovel.tipo.ilike('%casa%')).all()
        if found:
            answer = f"Encontrei {len(found)} casas. Quer ver por bairro?"
    elif 'preço' in q or 'valor' in q or 'até' in q or 'ate' in q:
        answer = "Me diga um valor alvo, por exemplo: 'até 600 mil em Jurerê'."
    return jsonify({"answer": answer})

@app.route('/admin')
def admin():
    q = request.args.get('q','')
    base = Imovel.query
    if q:
        like = f"%{q}%"
        base = base.filter(
            (Imovel.codigo.ilike(like)) | (Imovel.tipo.ilike(like)) |
            (Imovel.bairro.ilike(like)) | (Imovel.descricao.ilike(like))
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

@app.route('/admin/save', methods=['POST'])
def admin_save():
    form = request.form
    iid = form.get('id')
    if iid:
        obj = Imovel.query.get(int(iid))
        if not obj: return redirect('/admin')
    else:
        obj = Imovel()
        db.session.add(obj)

    obj.codigo = form.get('codigo')
    obj.tipo = form.get('tipo')
    try:
        obj.valor = float(form.get('valor').replace(',', '.'))
    except:
        obj.valor = 0.0
    obj.bairro = form.get('bairro')
    obj.imagem = form.get('imagem')
    obj.descricao = form.get('descricao')
    obj.status = form.get('status', 'ativo')

    db.session.commit()
    return redirect('/admin')

@app.route('/admin/export')
def admin_export():
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id','codigo','tipo','valor','bairro','descricao','imagem','status'])
    for i in Imovel.query.order_by(Imovel.id).all():
        writer.writerow([i.id, i.codigo, i.tipo, i.valor, i.bairro, (i.descricao or '').replace('\n',' '), i.imagem, i.status])
    output = si.getvalue().encode('utf-8')
    return send_file(
        io.BytesIO(output),
        mimetype='text/csv',
        as_attachment=True,
        download_name='imoveis.csv'
    )

@app.route('/admin/import', methods=['POST'])
def admin_import():
    file = request.files.get('csvfile')
    if not file: return redirect('/admin')
    stream = io.StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    count = 0
    for row in reader:
        codigo = row.get('codigo')
        if not codigo: continue
        obj = Imovel.query.filter_by(codigo=codigo).first() or Imovel()
        if not obj.id: db.session.add(obj)
        obj.codigo = codigo
        obj.tipo = row.get('tipo')
        try: obj.valor = float(row.get('valor') or 0)
        except: obj.valor = 0
        obj.bairro = row.get('bairro')
        obj.descricao = row.get('descricao')
        obj.imagem = row.get('imagem')
        obj.status = row.get('status') or 'ativo'
        count += 1
    db.session.commit()
    print(f"✅ Importados/atualizados: {count}")
    return redirect('/admin')

@app.route("/servicos", methods=["GET", "POST"])
def servicos():
    sucesso = False
    erro = None

    if request.method == "POST":
        try:
            # Captura dos dados do formulário
            nome = request.form.get("nome_cliente")
            telefone = request.form.get("telefone")
            imovel_id = request.form.get("imovel_id")
            tipo_servico = request.form.get("tipo_servico")
            descricao = request.form.get("descricao")

            # Validação do ID do imóvel
            imovel_id = int(imovel_id) if imovel_id and imovel_id.isdigit() else None

            # Criação do registro
            novo = Servico(
                nome_cliente=nome,
                telefone=telefone,
                imovel_id=imovel_id,
                tipo_servico=tipo_servico,
                descricao=descricao,
                data_solicitacao=datetime.datetime.now(),
                status="pendente",
            )

            db.session.add(novo)
            db.session.commit()
            sucesso = True

        except Exception as e:
            db.session.rollback()
            erro = str(e)
            print(f"❌ Erro ao salvar serviço: {erro}")

    # Carrega imóveis ativos para o select do formulário
    imoveis = Imovel.query.filter_by(status="ativo").order_by(Imovel.id.desc()).all()

    return render_template("servicos.html", sucesso=sucesso, erro=erro, imoveis=imoveis)


@app.route('/admin/servicos')
def admin_servicos():
    servicos = Servico.query.order_by(Servico.data_solicitacao.desc()).all()
    return render_template('admin_servicos.html', servicos=servicos)

@app.route('/admin/servicos/update/<int:id>', methods=['POST'])
def update_servico(id):
    s = Servico.query.get(id)
    s.status = request.form.get('status', s.status)
    s.data_agendamento = datetime.strptime(request.form.get('data_agendamento'), "%Y-%m-%d") if request.form.get('data_agendamento') else s.data_agendamento
    s.responsavel = request.form.get('responsavel')
    s.custo = request.form.get('custo') or 0
    s.materiais = request.form.get('materiais')
    db.session.commit()
    return redirect('/admin/servicos')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Banco de dados ok")
    app.run(debug=True)
