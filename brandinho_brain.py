# ============================================================
# brandinho_brain.py
# ------------------------------------------------------------
# Brandinho v1.3 - responde com base nos imóveis reais do banco
# ============================================================

from models import Imovel, db
import re

def responder(q: str) -> str:
    q = (q or "").lower().strip()
    if not q:
        return "Olá! 👋 Posso te ajudar a encontrar casas e apartamentos. Diga um bairro ou valor."

    # ============================================================
    # 🔍 INTERPRETAÇÃO BÁSICA (tipo, bairro, valor)
    # ============================================================
    tipos = ["casa", "apartamento", "apto", "cobertura", "terreno", "sala", "studio"]
    bairros = ["ratones", "canasvieiras", "jurere", "jurerê", "ingleses", "rio vermelho", "vargem"]
    tipo_encontrado = next((t for t in tipos if t in q), None)
    bairro_encontrado = next((b for b in bairros if b in q), None)

    # Extrair valor "até xxx mil"
    valor_max = None
    match_valor = re.search(r"(\d+[.,]?\d*)\s*(mil|milhão|milhoes|m)", q)
    if match_valor:
        num = match_valor.group(1).replace(",", ".")
        mult = 1000 if "mil" in match_valor.group(2) else 1_000_000
        valor_max = float(num) * mult

    # ============================================================
    # 🔎 CONSTRUÇÃO DE QUERY DINÂMICA
    # ============================================================
    query = Imovel.query.filter_by(status="ativo")

    if tipo_encontrado:
        query = query.filter(Imovel.tipo.ilike(f"%{tipo_encontrado}%"))
    if bairro_encontrado:
        query = query.filter(Imovel.bairro.ilike(f"%{bairro_encontrado}%"))
    if valor_max:
        query = query.filter(Imovel.valor <= valor_max)

    encontrados = query.limit(5).all()

    # ============================================================
    # 📊 GERAR RESPOSTA DINÂMICA
    # ============================================================
    if encontrados:
        resumo = ", ".join([f"{i.tipo} em {i.bairro} (R$ {i.valor:,.0f})" for i in encontrados])
        total = len(encontrados)
        if bairro_encontrado and tipo_encontrado:
            return f"Encontrei {total} {tipo_encontrado}{'s' if total>1 else ''} em {bairro_encontrado.capitalize()} 🏡: {resumo}."
        elif tipo_encontrado:
            return f"Tenho {total} {tipo_encontrado}{'s' if total>1 else ''} disponíveis em várias regiões de Floripa 🌴: {resumo}."
        elif bairro_encontrado:
            return f"Veja o que encontrei em {bairro_encontrado.capitalize()} 🌇: {resumo}."
        else:
            return f"Encontrei {total} imóveis disponíveis: {resumo}."

    # ============================================================
    # 🔁 RESPOSTAS GENÉRICAS
    # ============================================================
    if "comprar" in q:
        return "Comprar um imóvel é um ótimo investimento 🏡. Pode me dizer o bairro ou faixa de valor?"
    if "alugar" in q:
        return "Também temos opções de locação 🏠. Quer ver casas ou apartamentos?"
    if "serviço" in q or "reparo" in q or "manutenção" in q or "chamado" in q:
        return "Se você já comprou conosco, pode abrir um chamado em /servicos 🛠️."
    if "onde" in q or "endereço" in q or "fica" in q or "localização" in q:
        return "📍 Rua Intendente Antônio Damasco, 2330 - Ratones / Florianópolis."
    if "horario" in q or "funciona" in q or "atendimento" in q:
        return "Nosso atendimento é de segunda a sexta, das 9h às 18h 🕒."

    # ============================================================
    # 🔚 FALLBACK
    # ============================================================
    return "Ainda estou aprendendo 🧠, mas posso te ajudar com imóveis por tipo, bairro ou valor. Exemplo: 'apartamento até 600 mil em Canasvieiras'."
