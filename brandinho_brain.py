# ============================================================
# brandinho_brain.py
# ------------------------------------------------------------
# "Cérebro" do assistente Brandinho v1.1
# Contém as intenções e respostas padrões da Brando Imóveis.
# ------------------------------------------------------------
# Desenvolvido por Nous Tecnologia 💙  |  Outubro / 2025
# ============================================================

from models import Imovel, db

def responder(q: str) -> str:
    """
    Processa a mensagem do usuário e retorna a resposta do Brandinho.
    Versão 1.1 - Base fixa de intenções (sem banco de perguntas ainda).
    """
    q = (q or "").lower().strip()
    if not q:
        return "Olá! 👋 Posso te ajudar a encontrar casas e apartamentos. Diga um bairro ou valor."

    # ============================================================
    # COMPRA E VENDA
    # ============================================================
    if "comprar" in q or "venda" in q or "à venda" in q:
        return "Comprar um imóvel é um ótimo investimento 🏡. Posso te mostrar as opções disponíveis hoje?"
    if "financiamento" in q or "banco" in q or "entrada" in q:
        return "A Brando te orienta em todo o processo de financiamento 🏦. Trabalhamos com os principais bancos!"
    if "documento" in q or "documentação" in q:
        return "Fique tranquilo! A Brando te acompanha em todas as etapas de documentação do imóvel 📑."
    if "visita" in q or "agendar" in q or "ver imóvel" in q:
        return "Quer agendar uma visita? 😊 É só me dizer o código do imóvel ou o bairro que te interessa."

    # ============================================================
    # ALUGUEL
    # ============================================================
    if "alugar" in q or "locação" in q:
        return "Também trabalhamos com locações 🏘️. Quer ver imóveis para alugar em algum bairro específico?"
    if "contrato" in q:
        return "Os contratos de locação seguem padrões atualizados, com transparência e segurança para ambas as partes 🤝."

    # ============================================================
    # SERVIÇOS / PÓS-VENDA
    # ============================================================
    if "serviço" in q or "reparo" in q or "manutenção" in q or "chamado" in q:
        return "Se você já comprou conosco, pode abrir um chamado de serviço em /servicos 🛠️."
    if "reforma" in q or "pintura" in q or "hidráulica" in q or "elétrica" in q:
        return "A Brando conta com parceiros para reformas e manutenções. Podemos te indicar alguém 👍."

    # ============================================================
    # LOCALIZAÇÃO E BAIRROS
    # ============================================================
    if "ratones" in q:
        found = Imovel.query.filter(Imovel.bairro.ilike("%ratones%")).all()
        if found:
            lista = ", ".join([f"{i.tipo} {i.codigo} (R$ {i.valor:,.0f})" for i in found])
            return f"Ratones é um bairro tranquilo e cheio de natureza 🌳. Temos {len(found)} opções: {lista}."
        return "Ratones é um bairro tranquilo e cheio de natureza 🌳. No momento, não encontrei imóveis ativos lá."

    if "canas" in q:
        found = Imovel.query.filter(Imovel.bairro.ilike("%canas%")).all()
        if found:
            lista = ", ".join([f"{i.tipo} {i.codigo} (R$ {i.valor:,.0f})" for i in found])
            return f"Canasvieiras é ótimo para quem ama praia e praticidade 🌊. Temos {len(found)} opções: {lista}."
        return "Canasvieiras é ótimo para quem ama praia e praticidade 🌊. No momento não encontrei imóveis disponíveis."

    if "jurere" in q or "jurerê" in q:
        found = Imovel.query.filter(Imovel.bairro.ilike("%jur%")).all()
        if found:
            lista = ", ".join([f"{i.tipo} {i.codigo} (R$ {i.valor:,.0f})" for i in found])
            return f"Jurerê é uma excelente região para investimento 💎. Temos {len(found)} imóveis: {lista}."
        return "Jurerê é uma excelente região para investimento 💎. Ainda não temos imóveis cadastrados lá."

    if "bairro" in q:
        return "Temos imóveis em Ratones, Canasvieiras, Jurerê e outras regiões de Florianópolis 🗺️."

    # ============================================================
    # VALOR E FAIXA DE PREÇO
    # ============================================================
    if "preço" in q or "valor" in q or "mil" in q or "reais" in q or "até" in q or "ate" in q:
        return "Posso te ajudar a buscar imóveis por faixa de valor 💰. Exemplo: 'até 600 mil em Canasvieiras'."
    if "caro" in q or "barato" in q or "investimento" in q:
        return "Temos imóveis para todos os perfis — de oportunidades acessíveis a investimentos premium 💼."

    # ============================================================
    # INFORMAÇÕES GERAIS
    # ============================================================
    if "horário" in q or "funciona" in q or "aberto" in q or "atendimento" in q:
        return "Nosso atendimento é de segunda a sexta, das 9h às 18h 🕒, e aos sábados sob agendamento."
    if "endereço" in q or "localização" in q or "onde fica" in q:
        return "📍 Rua Intendente Antônio Damasco, 2330 - Ratones / Florianópolis."
    if "telefone" in q or "contato" in q or "whats" in q:
        return "Você pode falar com a gente pelo WhatsApp 📱 (48) 99105-4216."
    if "creci" in q:
        return "A Brando Imóveis atua regularmente com o CRECI 61150 🏠."

    # ============================================================
    # INSTITUCIONAL
    # ============================================================
    if "quem é" in q or "sobre" in q or "história" in q:
        return "A Brando Imóveis nasceu com propósito 💙 — unir tecnologia e confiança para facilitar a compra do seu imóvel."
    if "nous" in q or "tecnologia" in q:
        return "O site da Brando foi desenvolvido pela Nous Tecnologia ⚙️, trazendo inovação e propósito para o mercado imobiliário."

    # ============================================================
    # FALLBACK
    # ============================================================
    return "Posso te ajudar com imóveis, serviços, valores e bairros 🏘️. Diga, por exemplo: 'casas em Ratones' ou 'apartamentos até 600 mil em Canasvieiras'."
