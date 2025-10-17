# 🏡 Brando Imóveis – Protótipo v1.1

## 🎯 Objetivo

O projeto **Brando Imóveis** nasce como uma iniciativa de apoio ao grupo de empreendedores liderado por **Brando e Janaina**, com o apoio da **Nous Tecnologia**, para criar uma plataforma moderna e automatizada de **gestão imobiliária e pós-venda**.

A solução permite:
- Divulgação dinâmica de imóveis disponíveis;
- Captação de leads com retorno instantâneo via **WhatsApp**;
- Painel administrativo para **gestão de imóveis e solicitações de serviços**;
- Suporte ao cliente mesmo **após a venda**, com abertura de chamados de manutenção;
- Assistente virtual **Brandinho**, com respostas inteligentes e consulta dinâmica ao banco de imóveis.

---

## ⚙️ Stack Tecnológica

| Camada | Tecnologia | Descrição |
|--------|-------------|-----------|
| Backend | Flask + SQLAlchemy | Lógica de negócio e integração com MySQL |
| Frontend | HTML + TailwindCSS + Jinja2 | Interface moderna, responsiva e leve |
| Banco | MySQL (HostGator) | Armazenamento dos dados de imóveis, leads e serviços |
| Deploy | Render + GitHub | Hospedagem automatizada e CI/CD |
| Integração | WhatsApp API | Comunicação automática com clientes |
| Assistente Virtual | Flask JSON API | Respostas automáticas do “Brandinho” |

---

## 🧱 Estrutura do Projeto

```
brando_imoveis/
├── app.py                # Núcleo Flask e rotas principais
├── config.py             # Configuração do banco e variáveis de ambiente
├── models.py             # Modelos ORM (Imovel, Lead, Servico)
├── requirements.txt      # Dependências do projeto
├── Procfile              # Configuração do deploy no Render
├── templates/
│   ├── index.html               # Página principal com listagem
│   ├── imovel.html              # Página de detalhes do imóvel
│   ├── contato.html             # Formulário de contato
│   ├── servicos.html            # Página pública de solicitação de serviços
│   ├── admin.html               # Painel administrativo de imóveis
│   └── admin_servicos.html      # Painel administrativo de serviços
├── static/
│   ├── css/
│   │   └── main.css             # Estilos institucionais (paleta Brando)
│   ├── js/
│   │   └── script.js            # Interações do Brandinho e busca dinâmica
│   └── img/
│       └── brando_logo.png
└── utils/
    └── whatsapp_utils.py        # Utilitário para mensagens automáticas
```

---

## 💾 Configuração do Banco (HostGator)

1. Acesse o **phpMyAdmin** no painel HostGator.  
2. Crie um banco de dados, por exemplo: `brando_db`.  
3. Crie um usuário e conceda permissões totais.  
4. Configure no Render as variáveis de ambiente:

```bash
DB_USER=usuario_hostgator
DB_PASS=senha_hostgator
DB_NAME=brando_db
DB_HOST=mysql.hostgator.com
SECRET_KEY=brandoimoveis_secret
```

---

## 🚀 Deploy no Render

1. Crie um repositório no GitHub com o nome `brando-imoveis`.  
2. Faça push do código.  
3. No Render → **New Web Service** → Conecte ao GitHub.  
4. Configure:
   - **Runtime:** Python 3  
   - **Build Command:** `pip install -r requirements.txt`  
   - **Start Command:** `gunicorn app:app`
5. Configure as variáveis de ambiente e publique.  
6. O deploy é contínuo (CI/CD automático). ✅

---

## 🔗 Rotas Principais

| Rota | Método | Descrição |
|------|---------|-----------|
| `/` | GET | Página inicial com listagem dos imóveis ativos |
| `/imovel/<id>` | GET | Detalhes completos do imóvel |
| `/lead` | POST | Registro de interesse do cliente e redirecionamento ao WhatsApp |
| `/contato` | GET/POST | Formulário de contato geral |
| `/servicos` | GET/POST | Solicitação de serviços e manutenções |
| `/admin` | GET | Painel de administração de imóveis |
| `/admin/servicos` | GET | Painel administrativo de serviços e chamados |
| `/admin/servicos/update/<id>` | POST | Atualização de status, custos e agendamentos |
| `/api/brandinho` | POST | API do assistente virtual Brandinho (respostas automáticas) |

---

## 🧰 Módulo de Serviços

- Solicitação pública de manutenção, reforma ou reparo;  
- Registro completo (cliente, imóvel, tipo, descrição, data);  
- Vínculo opcional com imóvel cadastrado;  
- Painel de controle com:
  - Atualização de **status** (pendente, andamento, concluído);
  - Cadastro de **responsável**, **materiais** e **custos**;
  - Visualização rápida por cliente, imóvel e data;
  - **JOIN otimizado** entre tabelas para performance.  

---

## 🤖 Brandinho – Assistente Virtual

O **Brandinho** é o assistente digital da Brando Imóveis, com base em IA leve e integração direta ao banco de imóveis.

**Exemplos de interação:**
- “Casas em Canasvieiras”
- “Apartamentos até 600 mil”
- “Tem imóvel na região de Ratones?”

📡 **Endpoint:**  
`POST /api/brandinho`  

```json
{ "q": "casa em canasvieiras" }
```

📨 **Resposta:**
```json
{ "answer": "Tenho estas opções em Canasvieiras: Casa A001 (R$ 550.000), Apto B004 (R$ 620.000)..." }
```

---

## 📱 Integração WhatsApp

O redirecionamento é feito automaticamente com mensagem personalizada:

```
https://wa.me/554891054216?text=Olá! Tenho interesse no imóvel código A002
```

Também utilizada nos formulários de **contato** e **lead**.

---

## 🧩 Próximas Etapas

- Upload múltiplo de imagens por imóvel;  
- Filtros avançados (faixa de preço, tipo, bairro);  
- Relatórios de serviços e manutenções;  
- Dashboards de leads e conversões;  
- Expansão do **Brandinho** para IA conversacional completa;  
- Implementação de login e níveis de acesso.

---

## 🎨 Paleta Visual Institucional

| Cor | Hex | Descrição |
|------|------|-----------|
| 🩵 **Brando Blue** | `#557985` | Azul institucional principal |
| 💙 **Brando Light** | `#88A9B9` | Tom secundário e hover |
| 💚 **Brando Green** | `#22C55E` | Destaques e confirmações |
| 🩶 **Text / Fundo** | `#111827 / #F9FAFB` | Texto padrão e fundo claro |

> Paleta inspirada na marca Brando Imóveis e aplicada no layout via `main.css`.

---

## 👥 Equipe

- **Brando & Janaina** – Coordenação e visão do projeto  
- **Will (Nous / Netunna Tech)** – Arquitetura e Desenvolvimento  
- **Nous Tecnologia** – Implementação e suporte técnico  
- **Parceiros Locais** – Testes e feedback de operação  

---

📅 **Versão:** 1.1.0  
📆 **Data:** Outubro/2025  
📜 **Licença:** Projeto interno Nous / Netunna – uso demonstrativo  
✨ **Slogan:** *“Tecnologia com propósito, a serviço de pessoas.”*
