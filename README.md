# 🏡 Brando Imóveis – Protótipo v1

## 🎯 Objetivo
O projeto **Brando Imóveis** nasce como uma iniciativa de apoio ao grupo de empreendedores liderado por **Brando e Janaina**, com o apoio da **Nous Tech**, para criar uma plataforma moderna e automatizada de gestão imobiliária.

O sistema permite divulgar imóveis de forma dinâmica, captar leads com retorno via WhatsApp, e facilitar o controle administrativo — tudo com base no banco de dados MySQL hospedado no HostGator e deploy no Render.

---

## ⚙️ Stack Tecnológica

| Camada | Tecnologia | Descrição |
|--------|-------------|-----------|
| Backend | Flask + SQLAlchemy | API e lógica de negócio |
| Frontend | HTML + TailwindCSS | Interface responsiva e leve |
| Banco | MySQL (HostGator) | Armazenamento dos dados |
| Deploy | Render + GitHub | Hospedagem automatizada |
| Integração | WhatsApp | Retorno dinâmico para leads |

---

## 🧱 Estrutura do Projeto

```
brando_imoveis/
├── app.py                # Núcleo Flask com rotas
├── config.py             # Configuração e conexão MySQL
├── models.py             # Modelos do banco de dados
├── requirements.txt      # Dependências
├── Procfile              # Configuração para deploy Render
├── templates/            # Páginas HTML
│   ├── index.html
│   ├── imovel.html
│   ├── admin.html
│   └── login.html
├── static/               # CSS, JS e uploads
│   ├── css/
│   ├── js/
│   └── uploads/
└── utils/
    └── whatsapp_utils.py
```

---

## 💾 Configuração do Banco (HostGator)

1. Acesse o **phpMyAdmin** no painel HostGator.  
2. Crie um banco de dados, por exemplo: `brando_db`.  
3. Crie um usuário e conceda permissão total.  
4. Anote as credenciais e configure as variáveis no Render:

```
DB_USER=usuario_hostgator
DB_PASS=senha_hostgator
DB_NAME=brando_db
DB_HOST=mysql.hostgator.com
SECRET_KEY=brandoimoveis_secret
```

---

## 🚀 Deploy no Render

1. Crie um repositório no GitHub com o nome `brando-imoveis`.  
2. Suba os arquivos do projeto.  
3. No Render, clique em **New Web Service** → conecte ao GitHub.  
4. Selecione:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Configure as variáveis de ambiente (acima).
6. Deploy automático habilitado ✅

---

## 🔗 Rotas e APIs

| Rota | Método | Descrição |
|------|---------|-----------|
| `/` | GET | Página inicial com listagem de imóveis |
| `/imovel/<id>` | GET | Página com detalhes do imóvel |
| `/lead` | POST | Coleta dados do cliente e redireciona para WhatsApp |
| `/api/imoveis` | GET | Retorna lista de imóveis em formato JSON |

---

## 📱 Integração WhatsApp

O sistema redireciona automaticamente o visitante para o WhatsApp com uma mensagem personalizada, exemplo:

```
https://wa.me/5548999999999?text=Olá! Tenho interesse no imóvel código 123
```

---

## 🧩 Próximas Etapas

- Painel administrativo para cadastro e controle de imóveis;
- Filtros de busca por bairro, valor e tipo;
- Upload múltiplo de imagens;
- Relatórios de leads e estatísticas;
- Integração com IA “Ednna Broker”.

---

## 👥 Equipe
- **Brando & Janaina** – Coordenação dos Empreendedores  
- **Will (Nous / Netunna Tech)** – Arquitetura e Desenvolvimento  
- **Parceiros locais** – Testes e feedback de operação

---

**Versão:** 1.0.0  
**Data:** Outubro/2025  
**Licença:** Projeto interno Netunna / Nous – uso exclusivo de demonstração
