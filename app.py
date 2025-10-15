# =====================================================
#  BRANDO IMÓVEIS / NOUS - APP PRINCIPAL (v1.1)
# =====================================================
# Flask + SQLAlchemy + MySQL Connector (HostGator)
# =====================================================

from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from models import db, Imovel, Lead
import config

# -----------------------------------------------------
# Inicializa app Flask e configurações
# -----------------------------------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = config.SECRET_KEY

# Inicializa banco
db.init_app(app)

# -----------------------------------------------------
# Rotas principais
# -----------------------------------------------------
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
        mensagem = request.form['mensagem']
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

        msg = f"Olá! Tenho interesse no imóvel código {imovel_id}"
        return redirect(f"https://wa.me/5548999999999?text={msg}")

    except Exception as e:
        print("❌ Erro ao registrar lead:", e)
        return "Erro ao enviar lead.", 500


@app.route('/api/imoveis')
def api_imoveis():
    imoveis = Imovel.query.all()
    return jsonify([
        {
            "id": i.id,
            "codigo": i.codigo,
            "tipo": i.tipo,
            "valor": i.valor,
            "bairro": i.bairro,
            "descricao": i.descricao
        } for i in imoveis
    ])

# -----------------------------------------------------
# Execução local / Debug
# -----------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso.")
    app.run(debug=True, host="0.0.0.0", port=5000)
