from flask import Flask, render_template, request, redirect, jsonify
from config import *
from models import db, Imovel, Lead
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

@app.route('/')
def home():
    imoveis = Imovel.query.filter_by(status='ativo').all()
    return render_template('index.html', imoveis=imoveis)

@app.route('/imovel/<int:id>')
def imovel_detalhe(id):
    imovel = Imovel.query.get(id)
    return render_template('imovel.html', imovel=imovel)

@app.route('/lead', methods=['POST'])
def lead():
    nome = request.form['nome']
    telefone = request.form['telefone']
    mensagem = request.form['mensagem']
    imovel_id = request.form.get('imovel_id')

    novo_lead = Lead(nome=nome, telefone=telefone, mensagem=mensagem, imovel_id=imovel_id, data=datetime.now())
    db.session.add(novo_lead)
    db.session.commit()

    msg = f"Olá! Tenho interesse no imóvel código {imovel_id}"
    return redirect(f"https://wa.me/5548999999999?text={msg}")

@app.route('/api/imoveis')
def api_imoveis():
    imoveis = Imovel.query.all()
    return jsonify([{
        "id": i.id,
        "codigo": i.codigo,
        "tipo": i.tipo,
        "valor": i.valor,
        "bairro": i.bairro,
        "descricao": i.descricao
    } for i in imoveis])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
