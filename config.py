import os
from urllib.parse import quote_plus

# =====================================================
#  CONFIGURAÇÃO DE CONEXÃO - BRANDO IMÓVEIS / NOUS
# =====================================================

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
SECRET_KEY = os.getenv("SECRET_KEY")

# Codifica a senha (importante se houver @, #, %, etc.)
DB_PASS_ENCODED = quote_plus(DB_PASS) if DB_PASS else ""

# Monta a URI de conexão segura
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
